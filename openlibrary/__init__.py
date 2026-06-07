import logging
import random
from datetime import date, timedelta
from . import controllers
from . import models

_logger = logging.getLogger(__name__)

def post_init_hook(env):

    def get_random_book_by_library(library_id):
        # اعتبارسنجی library_id
        if not library_id:
            raise ValueError("Library ID is required")
        library = env['openlibrary.library'].browse(library_id)
        if not library:
            raise ValueError(f"Library with ID {library_id} does not exist")
        
        # پیدا کردن همه کتاب‌های آن کتابخانه
        # با توجه به مدل‌های شما، book_repository از طریق repository_id به library متصل می‌شود
        books = env['openlibrary.book_repository'].search([
            ('repository_id.library_id', '=', library_id),
            ('active', '=', True),
            ('status', '=', 'free')  # فقط کتاب‌های فعال
        ])
        
        if not books:
            raise ValueError(f"No books found in library {library.name} (ID: {library_id})")
        
        # انتخاب یک کتاب تصادفی
        random_book = random.choice(books)
        
        return random_book


    """
    این تابع بعد از نصب ماژول اجرا می‌شود
    نقش‌های گروه کتابخانه را به کاربر ادمین اضافه می‌کند
    """
    def add_group_to_user(u, g):
        """
        این تابع یک نقشه را به یک کاربر می دهد
        """
        if g.id not in u.group_ids.ids:
            u.write({'group_ids': [(4, g.id)]})
            _logger.info(f"Added group {g.name} to {u.display_name} .")      
    
    try:
        employee_group = env.ref('openlibrary.group_library_employee', raise_if_not_found=False)
        director_group = env.ref('openlibrary.group_libraries_director', raise_if_not_found=False)
        if not employee_group:
            _logger.warning(f"Could not find employee_group in OpenLibrary.")
        if not director_group:
            _logger.warning(f"Could not find director_group in OpenLibrary.")


        for u in env['res.users'].search([('group_ids', 'in', env.ref('base.group_system').id)]):
            add_group_to_user(u,employee_group)
            add_group_to_user(u, director_group)

    except Exception as e:
        _logger.warning(f"Could not assign groups to admin user: {e}")

    # اضافه کردن مشترکین
    # جهت ایجاد تاریخ اتفاقی 
    def random_date(start_year=1950, end_year=2019):
            year = random.randint(start_year, end_year)
            month = random.randint(1, 12)
            
            # تعداد روزهای هر ماه
            month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            # محاسبه سال کبیسه
            if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                day = random.randint(1, 29)  # سال کبیسه (فوریه 29 روزه)
            else:
                day = random.randint(1, month_days[month - 1])
    
            return date(year, month, day)

    # دریافت همه کاربران فعال سیستم
    users = env['res.users'].search([('active', '=', True)])
    
    created_count = 0
    lent_state = [0, 1, 2, 3, 0, 1, 2, 0, 1, 0]
    cnt_state = 0

    for user in users:
        # بررسی اینکه آیا قبلاً subscriber برای این کاربر وجود دارد
        existing_subscriber = env['openlibrary.subscriber'].search([
            ('partner_id', '=', user.partner_id.id)
        ], limit=1)
        
        if not existing_subscriber:
            try:
                # ایجاد subscriber جدید
                sub = env['openlibrary.subscriber'].create({
                    'name': user.name,
                    'partner_id': user.partner_id.id,
                    'birthday': random_date(),
                    'active': True,
                })
                created_count += 1
                _logger.info(f"Created subscriber for user: {user.name} (ID: {user.id})")

                # اضافه کردن عضویت در سامانه
                main_lib = env['openlibrary.library'].search([('name', '=', 'Main Library')])
                city_lib = env['openlibrary.library'].search([('name', '=', 'City Library')])
                if created_count % 2:
                    lib = main_lib
                else:
                    lib = city_lib

                try:
                    if lib:
                        member = env['openlibrary.membership'].create({
                            'subscriber_id': sub.id,
                            'library_id': lib.id,
                        })
                        _logger.info(f"Add Subscribe '{sub.name}' to library '{lib.name}' (Membership: {member.id})")

                        # اضافه کردن کتاب امانت گرفته شده
                        if member:
                            # اضافه کردن یک تا سه کتاب 
                            for cnt in range(0, random.randint(1,3)):
                                # پیدا کردن یک کتاب آزاد در مخزن کتابهای که مشترک عضو آن است
                                book = get_random_book_by_library(lib.id)
                                randdate = date.today()
                                match(lent_state[cnt_state]):
                                    case 0:
                                        randdate += timedelta(days=-random.randint(0,10))
                                    case 1:
                                        randdate += timedelta(days=-random.randint(11,13))
                                    case 2:
                                        randdate += timedelta(days=-random.randint(13,30))
                                    case 3:
                                        randdate += timedelta(days=-random.randint(30,90))
                                cnt_state = (cnt_state + 1) % (len(lent_state))

                                if book:
                                    env['openlibrary.lend'].create({
                                        'subscriber_id' : sub.id,
                                        'book_repo_id' : book.id,
                                        'start_date': randdate
                                    })
                                    _logger.info(f"Lent book '{book.name}' to '{sub.name}' in {randdate}")
                except Exception as e:
                    _logger.warning(f"Cound not create membership for subscriber '{sub.name}' in library '{lib.name}': {e}")
            except Exception as e:
                _logger.warning(f"Could not create subscriber for user {user.name}: {e}")
    
    if created_count:
        _logger.info(f"✅ Successfully created {created_count} new subscribers")
    else:
        _logger.info("No new subscribers were created")

def pre_init_hook(cr):
    """
    این تابع قبل از نصب ماژول اجرا می‌شود
    """
    _logger.info("Pre-init hook for openlibrary module")