"""Seed data for Bearded Hop Brewery CRM - translates mockData.ts to Python."""
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.deps import get_password_hash


def _id(name: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_DNS, name)


async def run_seed(db: AsyncSession):
    await db.execute(text("""
        TRUNCATE TABLE order_timelines, service_alerts, floor_tables,
        pos_transactions, transaction_items, tab_items, open_tabs,
        wholesale_orders, wholesale_accounts, mug_club_members,
        email_campaigns, content_calendar, customer_segments, social_metrics,
        ttb_reports, monthly_financials, daily_sales, compliance_items,
        business_settings, schedule_shifts, staff_certifications, staff_members,
        purchase_orders, inventory_items, menu_items, reservations,
        events, performers, keg_events, kegs, tap_lines, gravity_readings,
        batches, detailed_recipes, recipes, visit_records, customer_notes,
        customers, beers, users CASCADE
    """))

    from app.models.user import User
    from app.models.customer import Customer
    from app.models.beer import Beer
    from app.models.recipe import Recipe
    from app.models.detailed_recipe import DetailedRecipe
    from app.models.batch import Batch
    from app.models.tap_line import TapLine
    from app.models.keg import Keg
    from app.models.performer import Performer
    from app.models.event import Event
    from app.models.reservation import Reservation
    from app.models.menu_item import MenuItem
    from app.models.inventory_item import InventoryItem
    from app.models.purchase_order import PurchaseOrder
    from app.models.staff_member import StaffMember
    from app.models.wholesale_account import WholesaleAccount
    from app.models.wholesale_order import WholesaleOrder
    from app.models.mug_club_member import MugClubMember
    from app.models.email_campaign import EmailCampaign
    from app.models.daily_sales import DailySales
    from app.models.monthly_financial import MonthlyFinancial
    from app.models.ttb_report import TTBReport
    from app.models.compliance_item import ComplianceItem
    from app.models.social_metrics import SocialMetrics
    from app.models.content_calendar import ContentCalendar
    from app.models.customer_segment import CustomerSegment
    from app.models.business_settings import BusinessSettings
    from app.models.open_tab import OpenTab
    from app.models.pos_transaction import POSTransaction
    from app.models.floor_table import FloorTable
    from app.models.service_alert import ServiceAlert
    from app.models.order_timeline import OrderTimeline

    # 1. Admin user
    admin = User(
        id=_id("admin"), email="admin@beardedhop.com",
        hashed_password=get_password_hash("BrewDay2026!"),
        first_name="Admin", last_name="Brewer", is_active=True, is_superuser=True,
    )
    db.add(admin)

    # 2. Customers
    customers = [
        Customer(id=_id("customer-1"), first_name="Jake", last_name="Morrison", email="jake@email.com", phone="(830) 555-0101", first_visit="2026-01-15", last_visit="2026-03-02", total_visits=24, total_spent=1842.50, avg_ticket=76.77, favorite_beers=["Hill Country Haze", "Bulverde Blonde"], dietary_restrictions=[], tags=["regular", "vip"], loyalty_points=2450, loyalty_tier="Gold", mug_club_member=True, mug_club_tier="Premium", notes="Loves IPAs, brings family every Saturday", source="word-of-mouth", family_members=[{"name": "Sarah", "relation": "wife"}, {"name": "Max", "relation": "son", "age": 7}]),
        Customer(id=_id("customer-2"), first_name="Maria", last_name="Gonzalez", email="maria.g@email.com", phone="(830) 555-0102", first_visit="2026-02-01", last_visit="2026-03-03", total_visits=16, total_spent=987.25, avg_ticket=61.70, favorite_beers=["Texas Sunset Wheat", "Prickly Pear Sour"], dietary_restrictions=["gluten-free options"], tags=["regular"], loyalty_points=1200, loyalty_tier="Silver", mug_club_member=True, mug_club_tier="Standard", notes="Prefers patio seating", source="instagram"),
        Customer(id=_id("customer-3"), first_name="Tom", last_name="Henderson", email="tom.h@email.com", phone="(830) 555-0103", first_visit="2026-01-20", last_visit="2026-03-04", total_visits=20, total_spent=1456.00, avg_ticket=72.80, favorite_beers=["Lone Star Lager", "Mesquite Smoked Porter"], dietary_restrictions=[], tags=["regular", "trivia-regular"], loyalty_points=1800, loyalty_tier="Gold", mug_club_member=False, notes="Trivia night captain", source="event"),
        Customer(id=_id("customer-4"), first_name="Ashley", last_name="Chen", email="ashley.c@email.com", phone="(830) 555-0104", first_visit="2026-02-14", last_visit="2026-03-01", total_visits=6, total_spent=312.50, avg_ticket=52.08, favorite_beers=["Craft Root Beer", "Hill Country Kombucha"], dietary_restrictions=["no alcohol"], tags=["new", "family"], loyalty_points=400, loyalty_tier="Bronze", mug_club_member=False, notes="Non-drinker, loves NA options", source="google"),
        Customer(id=_id("customer-5"), first_name="Bobby", last_name="Whitfield", email="bobby.w@email.com", phone="(830) 555-0105", first_visit="2025-12-01", last_visit="2026-03-05", total_visits=32, total_spent=2890.00, avg_ticket=90.31, favorite_beers=["Barrel-Aged Imperial Stout", "Hill Country Haze"], dietary_restrictions=[], tags=["regular", "vip", "whale-hunter"], loyalty_points=3200, loyalty_tier="Platinum", mug_club_member=True, mug_club_tier="Founding", notes="Beer whale, collects rare releases", source="untappd"),
        Customer(id=_id("customer-6"), first_name="Diane", last_name="Foster", email="diane.f@email.com", phone="(830) 555-0106", first_visit="2026-02-10", last_visit="2026-03-02", total_visits=8, total_spent=524.00, avg_ticket=65.50, favorite_beers=["Texas Sunset Wheat", "Bulverde Blonde"], dietary_restrictions=[], tags=["family"], loyalty_points=650, loyalty_tier="Bronze", mug_club_member=False, notes="Brings kids every weekend", source="facebook"),
        Customer(id=_id("customer-7"), first_name="Carlos", last_name="Rivera", email="carlos.r@email.com", phone="(830) 555-0107", first_visit="2026-01-08", last_visit="2026-03-05", total_visits=18, total_spent=1134.00, avg_ticket=63.00, favorite_beers=["Mesquite Smoked Porter", "Jalapeño Cream Ale"], dietary_restrictions=[], tags=["regular"], loyalty_points=1400, loyalty_tier="Silver", mug_club_member=False, notes="Loves dark and spicy beers", source="word-of-mouth"),
        Customer(id=_id("customer-8"), first_name="Linda", last_name="Thompson", email="linda.t@email.com", phone="(830) 555-0108", first_visit="2026-02-20", last_visit="2026-03-03", total_visits=4, total_spent=186.00, avg_ticket=46.50, favorite_beers=["Ginger Beer", "Craft Root Beer"], dietary_restrictions=["vegan"], tags=["new"], loyalty_points=250, loyalty_tier="Bronze", mug_club_member=False, notes="Vegan, prefers NA beverages", source="yelp"),
    ]
    db.add_all(customers)

    # 3. Beers
    beers = [
        Beer(id=_id("beer-1"), name="Hill Country Haze", style="New England IPA", abv=6.8, ibu=55, srm=6, description="A juicy, hazy IPA bursting with tropical fruit flavors", tasting_notes="Mango, pineapple, stone fruit with a soft, pillowy mouthfeel", food_pairings=["Spicy wings", "Fish tacos", "Citrus salad"], status="on-tap", tap_number=1, keg_level=72, rating=4.6, total_pours=1247, category="flagship"),
        Beer(id=_id("beer-2"), name="Lone Star Lager", style="American Lager", abv=4.8, ibu=18, srm=3, description="A crisp, clean lager perfect for Texas heat", tasting_notes="Light bread, subtle hop, clean finish", food_pairings=["Burgers", "BBQ", "Nachos"], status="on-tap", tap_number=2, keg_level=85, rating=4.2, total_pours=1891, category="flagship"),
        Beer(id=_id("beer-3"), name="Bulverde Blonde", style="Cream Ale", abv=5.0, ibu=22, srm=4, description="Our flagship blonde, smooth and approachable", tasting_notes="Light honey, biscuit, gentle sweetness", food_pairings=["Grilled chicken", "Light salads", "Pretzels"], status="on-tap", tap_number=3, keg_level=58, rating=4.4, total_pours=2103, category="flagship"),
        Beer(id=_id("beer-4"), name="Texas Sunset Wheat", style="American Wheat", abv=4.5, ibu=15, srm=5, description="A refreshing wheat beer with orange peel and coriander", tasting_notes="Orange zest, wheat bread, light spice", food_pairings=["Fish tacos", "Garden salad", "Fruit plate"], status="on-tap", tap_number=4, keg_level=65, rating=4.3, total_pours=987, category="flagship"),
        Beer(id=_id("beer-5"), name="Mesquite Smoked Porter", style="Smoked Porter", abv=6.2, ibu=35, srm=30, description="Rich porter smoked with Texas mesquite wood", tasting_notes="Mesquite smoke, chocolate, dark fruit", food_pairings=["Smoked brisket", "Dark chocolate", "Smoked gouda"], status="on-tap", tap_number=5, keg_level=44, rating=4.5, total_pours=756, category="flagship"),
        Beer(id=_id("beer-6"), name="Prickly Pear Sour", style="Berliner Weisse", abv=4.2, ibu=8, srm=4, description="A tart, fruity sour with local prickly pear cactus", tasting_notes="Prickly pear, lemon, tart candy", food_pairings=["Ceviche", "Goat cheese", "Fruit desserts"], status="on-tap", tap_number=6, keg_level=38, rating=4.4, total_pours=834, category="seasonal"),
        Beer(id=_id("beer-7"), name="Jalapeño Cream Ale", style="Spiced Cream Ale", abv=5.2, ibu=20, srm=4, description="Cream ale with fresh jalapeño — mild heat, big flavor", tasting_notes="Fresh jalapeño, cream, slight heat on finish", food_pairings=["Nachos", "Tacos", "Quesadillas"], status="on-tap", tap_number=7, keg_level=82, rating=4.1, total_pours=623, category="flagship"),
        Beer(id=_id("beer-8"), name="Bluebonnet Blonde", style="Belgian Blonde", abv=6.5, ibu=25, srm=5, description="Belgian-inspired blonde with fruity esters", tasting_notes="Pear, banana, light pepper, dry finish", food_pairings=["Mussels", "Brie cheese", "Roasted chicken"], status="on-tap", tap_number=8, keg_level=91, rating=4.3, total_pours=445, category="seasonal"),
        Beer(id=_id("beer-9"), name="Citra Smash IPA", style="SMaSH IPA", abv=6.5, ibu=60, srm=5, description="Single malt, single hop IPA showcasing Citra", tasting_notes="Grapefruit, lime, passion fruit, clean bitter finish", food_pairings=["Spicy Thai", "Grilled shrimp", "Citrus desserts"], status="on-tap", tap_number=9, keg_level=55, rating=4.5, total_pours=567, category="limited"),
        Beer(id=_id("beer-10"), name="Barrel-Aged Imperial Stout", style="Imperial Stout", abv=11.5, ibu=45, srm=40, description="Imperial stout aged in bourbon barrels for 6 months", tasting_notes="Bourbon, vanilla, dark chocolate, oak, roasted coffee", food_pairings=["Dark chocolate cake", "Blue cheese", "Crème brûlée"], status="on-tap", tap_number=10, keg_level=28, rating=4.8, total_pours=312, category="limited"),
        Beer(id=_id("beer-11"), name="Craft Root Beer", style="Root Beer", abv=0, ibu=0, srm=20, description="House-made craft root beer with real sassafras", tasting_notes="Sassafras, vanilla, wintergreen, smooth cream", food_pairings=["Burgers", "Ice cream floats", "Kids meals"], status="on-tap", tap_number=11, keg_level=70, rating=4.7, total_pours=432, category="flagship", is_non_alcoholic=True),
        Beer(id=_id("beer-12"), name="Ginger Beer", style="Ginger Beer", abv=0, ibu=0, srm=8, description="Spicy ginger beer brewed with fresh ginger root", tasting_notes="Fresh ginger, lemon, light honey", food_pairings=["Sushi", "Grilled fish", "Moscow Mule base"], status="on-tap", tap_number=12, keg_level=60, rating=4.3, total_pours=289, category="flagship", is_non_alcoholic=True),
        Beer(id=_id("beer-13"), name="Hill Country Kombucha", style="Kombucha", abv=0.5, ibu=0, srm=6, description="House-brewed kombucha with local honey and fruit", tasting_notes="Tart apple, honey, effervescent, light funk", food_pairings=["Salads", "Grain bowls", "Light appetizers"], status="on-tap", tap_number=13, keg_level=48, rating=4.1, total_pours=198, category="flagship", is_non_alcoholic=True),
        Beer(id=_id("beer-14"), name="Spring Saison", style="Saison", abv=6.8, ibu=28, srm=5, description="Farmhouse ale with spring botanicals", tasting_notes="Lemon zest, white pepper, floral, bone dry", food_pairings=["Grilled vegetables", "Soft cheese", "Herb roasted chicken"], status="fermenting", rating=0, total_pours=0, category="seasonal"),
        Beer(id=_id("beer-15"), name="Peach Wheat", style="Fruit Wheat", abv=4.8, ibu=12, srm=4, description="Wheat beer with Fredericksburg peaches", tasting_notes="Fresh peach, wheat, light sweetness", food_pairings=["Peach cobbler", "Grilled chicken", "Summer salads"], status="conditioning", rating=0, total_pours=0, category="seasonal"),
    ]
    db.add_all(beers)

    # 4. Batches
    batches = [
        Batch(id=_id("batch-1"), batch_number="BH-2026-012", beer_id=_id("beer-3"), beer_name="Bulverde Blonde", style="Cream Ale", status="ready", brew_date="2026-02-15", target_og=1.050, actual_og=1.051, target_fg=1.010, actual_fg=1.010, abv=5.1, tank_id="FV-1", volume=7, notes="Flagship batch", gravity_readings=[{"date": "2026-02-16", "gravity": 1.051, "temp": 66}, {"date": "2026-02-18", "gravity": 1.032, "temp": 66}, {"date": "2026-02-22", "gravity": 1.012, "temp": 67}, {"date": "2026-02-25", "gravity": 1.010, "temp": 67}], temperature_log=[], quality_score=95),
        Batch(id=_id("batch-2"), batch_number="BH-2026-013", beer_id=_id("beer-14"), beer_name="Spring Saison", style="Saison", status="fermenting", brew_date="2026-02-28", target_og=1.060, actual_og=1.062, target_fg=1.004, tank_id="FV-2", volume=7, notes="Spring release", gravity_readings=[{"date": "2026-02-28", "gravity": 1.062, "temp": 68}, {"date": "2026-03-02", "gravity": 1.038, "temp": 72}], temperature_log=[]),
        Batch(id=_id("batch-3"), batch_number="BH-2026-014", beer_id=_id("beer-15"), beer_name="Peach Wheat", style="Fruit Wheat", status="conditioning", brew_date="2026-02-20", target_og=1.048, actual_og=1.049, target_fg=1.010, actual_fg=1.011, abv=4.9, tank_id="FV-3", volume=7, notes="Fredericksburg peaches added day 5", gravity_readings=[{"date": "2026-02-20", "gravity": 1.049, "temp": 65}, {"date": "2026-02-25", "gravity": 1.011, "temp": 66}], temperature_log=[], quality_score=88),
        Batch(id=_id("batch-4"), batch_number="BH-2026-015", beer_id=_id("beer-1"), beer_name="Hill Country Haze", style="New England IPA", status="carbonating", brew_date="2026-02-22", target_og=1.065, actual_og=1.066, target_fg=1.014, actual_fg=1.013, abv=6.9, tank_id="BT-1", volume=7, notes="Extra dry hop addition", gravity_readings=[{"date": "2026-02-22", "gravity": 1.066, "temp": 67}, {"date": "2026-02-26", "gravity": 1.028, "temp": 68}, {"date": "2026-03-01", "gravity": 1.013, "temp": 68}], temperature_log=[], quality_score=92),
    ]
    db.add_all(batches)

    # 5. Tap Lines
    tap_lines = []
    pour_sizes = [{"name": "Taster", "oz": 5, "price": 3}, {"name": "Half", "oz": 10, "price": 5}, {"name": "Pint", "oz": 16, "price": 7}, {"name": "Growler", "oz": 64, "price": 14}]
    mug_pour_sizes = [{"name": "Taster", "oz": 5, "price": 3}, {"name": "Half", "oz": 10, "price": 5}, {"name": "Pint", "oz": 16, "price": 7}, {"name": "Mug Club 20oz", "oz": 20, "price": 7}, {"name": "Growler", "oz": 64, "price": 14}]
    for i, beer in enumerate(beers[:13], 1):
        tap_lines.append(TapLine(
            tap_number=i, beer_id=beer.id, beer_name=beer.name, style=beer.style,
            abv=beer.abv, ibu=beer.ibu, keg_level=beer.keg_level or 100,
            keg_size="1/2", status="active",
            pour_sizes=mug_pour_sizes if i <= 10 else pour_sizes,
            total_pours=beer.total_pours, revenue_today=round(beer.total_pours * 0.15, 2),
        ))
    db.add_all(tap_lines)

    # 6. Performers
    performers = [
        Performer(id=_id("performer-1"), name="Coyote Creek Band", genre="Country/Red Dirt", contact_email="coyotecreek@music.com", contact_phone="(512) 555-0201", fee=800, rating=4.8, past_performances=12, bio="Local 4-piece country band, crowd favorite", social_links=[{"platform": "instagram", "url": "https://instagram.com/coyotecreekband"}]),
        Performer(id=_id("performer-2"), name="Tres Amigos", genre="Tejano/Latin", contact_email="tresamigos@music.com", contact_phone="(210) 555-0202", fee=600, rating=4.5, past_performances=8, bio="Tejano trio bringing the energy", social_links=[]),
        Performer(id=_id("performer-3"), name="Blue Highway", genre="Americana/Bluegrass", contact_email="bluehighway@music.com", contact_phone="(512) 555-0203", fee=1000, rating=4.9, past_performances=6, bio="Award-winning bluegrass quartet from Austin", social_links=[]),
        Performer(id=_id("performer-4"), name="Sarah & the Songbirds", genre="Indie Folk", contact_email="sarah@songbirds.com", contact_phone="(830) 555-0204", fee=500, rating=4.6, past_performances=15, bio="Local singer-songwriter duo", social_links=[]),
        Performer(id=_id("performer-5"), name="DJ Tex", genre="DJ/Electronic", contact_email="djtex@email.com", contact_phone="(512) 555-0205", fee=400, rating=4.2, past_performances=4, bio="Mix master for special events", social_links=[]),
    ]
    db.add_all(performers)

    # 7. Events
    events = [
        Event(id=_id("event-1"), title="Coyote Creek Band Live", type="live-music", date="2026-03-07", start_time="7:00 PM", end_time="10:00 PM", description="Friday night live music on the patio", performer_id=_id("performer-1"), capacity=120, tickets_sold=0, ticket_price=0, is_ticketed=False, is_family_friendly=True, location="patio", status="upcoming", revenue=0),
        Event(id=_id("event-2"), title="Tuesday Trivia Night", type="trivia", date="2026-03-04", start_time="7:00 PM", end_time="9:00 PM", description="Weekly pub trivia with prizes", capacity=80, tickets_sold=0, ticket_price=0, is_ticketed=False, is_family_friendly=True, location="taproom", status="completed", revenue=1245),
        Event(id=_id("event-3"), title="Spring Saison Release Party", type="beer-release", date="2026-03-15", start_time="4:00 PM", end_time="9:00 PM", description="First pour of our Spring Saison", capacity=100, tickets_sold=42, ticket_price=15, is_ticketed=True, is_family_friendly=True, location="beer-garden", status="upcoming", revenue=0, special_beer="Spring Saison"),
        Event(id=_id("event-4"), title="Kids Craft & Brew Saturday", type="family", date="2026-03-08", start_time="11:00 AM", end_time="3:00 PM", description="Crafts for kids while parents enjoy brews", capacity=50, tickets_sold=0, ticket_price=0, is_ticketed=False, is_family_friendly=True, location="beer-garden", status="upcoming", revenue=0),
        Event(id=_id("event-5"), title="Tres Amigos Tejano Night", type="live-music", date="2026-03-14", start_time="7:00 PM", end_time="10:00 PM", description="Tejano music and tacos on the patio", performer_id=_id("performer-2"), capacity=120, tickets_sold=0, ticket_price=0, is_ticketed=False, is_family_friendly=True, location="patio", status="upcoming", revenue=0),
        Event(id=_id("event-6"), title="Beer & BBQ Pairing Dinner", type="pairing-dinner", date="2026-03-21", start_time="6:30 PM", end_time="9:00 PM", description="5-course BBQ pairing with our beers", capacity=40, tickets_sold=28, ticket_price=65, is_ticketed=True, is_family_friendly=False, location="event-hall", status="upcoming", revenue=0),
        Event(id=_id("event-7"), title="Private Wedding Reception", type="private", date="2026-03-22", start_time="5:00 PM", end_time="11:00 PM", description="Johnson-Williams wedding reception", capacity=80, tickets_sold=80, ticket_price=0, is_ticketed=False, is_family_friendly=True, location="event-hall", status="upcoming", revenue=3500),
        Event(id=_id("event-8"), title="Blue Highway Bluegrass", type="live-music", date="2026-03-28", start_time="7:00 PM", end_time="10:00 PM", description="Award-winning bluegrass from Austin", performer_id=_id("performer-3"), capacity=150, tickets_sold=67, ticket_price=20, is_ticketed=True, is_family_friendly=True, location="beer-garden", status="upcoming", revenue=0),
    ]
    db.add_all(events)

    from app.models.event import Event as _  # already imported

    # 8. Reservations
    reservations = [
        Reservation(id=_id("res-1"), customer_name="Jake Morrison", customer_phone="(830) 555-0101", customer_email="jake@email.com", date="2026-03-05", time="7:30 PM", party_size=4, table_id="T-4", section="taproom", status="confirmed", notes="Birthday dinner", special_requests=["Birthday cake", "Window seat"], is_high_chair_needed=False),
        Reservation(id=_id("res-2"), customer_name="Sarah Williams", customer_phone="(830) 555-0201", customer_email="sarah.w@email.com", date="2026-03-05", time="6:00 PM", party_size=6, table_id="P-3", section="patio", status="confirmed", notes="Anniversary", special_requests=[], is_high_chair_needed=False),
        Reservation(id=_id("res-3"), customer_name="Corporate Group", customer_phone="(830) 555-0301", customer_email="events@company.com", date="2026-03-05", time="5:00 PM", party_size=20, table_id="R-1", section="private-room", status="confirmed", notes="Team building event", special_requests=["Projector", "Appetizer platter"], is_high_chair_needed=False),
        Reservation(id=_id("res-4"), customer_name="Diane Foster", customer_phone="(830) 555-0106", customer_email="diane.f@email.com", date="2026-03-06", time="12:00 PM", party_size=5, section="patio", status="confirmed", notes="Kids birthday party", special_requests=["High chairs x2"], is_high_chair_needed=True),
        Reservation(id=_id("res-5"), customer_name="Walk-in", customer_phone="", date="2026-03-05", time="8:00 PM", party_size=2, section="taproom", status="waitlist", notes="", special_requests=[], is_high_chair_needed=False),
    ]
    db.add_all(reservations)

    from app.models.reservation import Reservation as __

    # 9. Menu Items
    menu_items = [
        MenuItem(id=_id("menu-1"), name="Smoked Wings (8pc)", description="Mesquite-smoked wings with ranch or blue cheese", category="appetizer", price=14.99, cost=4.50, is_available=True, allergens=[], dietary_tags=["gluten-free"], is_kids_friendly=False, popularity=92),
        MenuItem(id=_id("menu-2"), name="Brew Cheese & Pretzel Board", description="House beer cheese with soft pretzels and mustard", category="appetizer", price=13.99, cost=3.80, is_available=True, allergens=["dairy", "gluten"], dietary_tags=["vegetarian"], is_kids_friendly=True, popularity=88),
        MenuItem(id=_id("menu-3"), name="Loaded Nachos", description="Tortilla chips, queso, jalapeños, pico, sour cream", category="appetizer", price=12.99, cost=3.20, is_available=True, allergens=["dairy"], dietary_tags=["vegetarian"], is_kids_friendly=True, popularity=85),
        MenuItem(id=_id("menu-4"), name="Jalapeño Poppers", description="Cream cheese stuffed jalapeños, beer-battered", category="appetizer", price=11.99, cost=3.00, is_available=True, allergens=["dairy", "gluten"], dietary_tags=[], is_kids_friendly=False, popularity=78),
        MenuItem(id=_id("menu-5"), name="Brewhouse Burger", description="Half-pound Angus patty, beer cheese, bacon, brioche bun", category="entree", price=16.99, cost=5.50, is_available=True, allergens=["dairy", "gluten"], dietary_tags=[], is_kids_friendly=False, popularity=95),
        MenuItem(id=_id("menu-6"), name="Smoked Brisket Plate", description="14-hour smoked brisket, coleslaw, pickles, bread", category="entree", price=19.99, cost=7.00, is_available=True, allergens=["gluten"], dietary_tags=["gluten-free option"], is_kids_friendly=False, popularity=90),
        MenuItem(id=_id("menu-7"), name="Fish Tacos", description="Beer-battered cod, cabbage slaw, chipotle crema", category="entree", price=15.99, cost=5.00, is_available=True, allergens=["fish", "gluten"], dietary_tags=[], is_kids_friendly=False, popularity=82),
        MenuItem(id=_id("menu-8"), name="BBQ Pulled Pork Sandwich", description="Slow-smoked pulled pork, house BBQ sauce, coleslaw", category="entree", price=14.99, cost=4.50, is_available=True, allergens=["gluten"], dietary_tags=[], is_kids_friendly=False, popularity=86),
        MenuItem(id=_id("menu-9"), name="Grilled Veggie Bowl", description="Roasted seasonal vegetables, quinoa, tahini dressing", category="entree", price=13.99, cost=3.50, is_available=True, allergens=["sesame"], dietary_tags=["vegan", "gluten-free"], is_kids_friendly=True, popularity=72),
        MenuItem(id=_id("menu-10"), name="Loaded Fries", description="Beer cheese, bacon, jalapeños, ranch", category="side", price=8.99, cost=2.00, is_available=True, allergens=["dairy"], dietary_tags=[], is_kids_friendly=True, popularity=88),
        MenuItem(id=_id("menu-11"), name="Coleslaw", description="House-made creamy coleslaw", category="side", price=4.99, cost=0.80, is_available=True, allergens=["dairy"], dietary_tags=["vegetarian", "gluten-free"], is_kids_friendly=True, popularity=65),
        MenuItem(id=_id("menu-12"), name="Stout Brownie Sundae", description="Chocolate stout brownie, vanilla ice cream, hot fudge", category="dessert", price=10.99, cost=3.00, is_available=True, allergens=["dairy", "gluten", "eggs"], dietary_tags=[], is_kids_friendly=True, popularity=91),
        MenuItem(id=_id("menu-13"), name="Kids Chicken Tenders", description="Breaded chicken tenders with fries", category="kids", price=8.99, cost=2.50, is_available=True, allergens=["gluten"], dietary_tags=[], is_kids_friendly=True, popularity=94),
        MenuItem(id=_id("menu-14"), name="Kids Mac & Cheese", description="Creamy mac and cheese", category="kids", price=7.99, cost=1.50, is_available=True, allergens=["dairy", "gluten"], dietary_tags=["vegetarian"], is_kids_friendly=True, popularity=92),
        MenuItem(id=_id("menu-15"), name="Kids Grilled Cheese", description="Classic grilled cheese on sourdough", category="kids", price=7.99, cost=1.20, is_available=True, allergens=["dairy", "gluten"], dietary_tags=["vegetarian"], is_kids_friendly=True, popularity=88),
        MenuItem(id=_id("menu-16"), name="Lavender Lemonade", description="Fresh lemonade with lavender syrup", category="beverage-na", price=5.99, cost=1.00, is_available=True, allergens=[], dietary_tags=["vegan", "gluten-free"], is_kids_friendly=True, popularity=80),
        MenuItem(id=_id("menu-17"), name="Watermelon Agua Fresca", description="Fresh watermelon, lime, mint", category="beverage-na", price=5.99, cost=1.00, is_available=True, allergens=[], dietary_tags=["vegan", "gluten-free"], is_kids_friendly=True, popularity=76),
        MenuItem(id=_id("menu-18"), name="BH Logo T-Shirt", description="Bearded Hop Brewery logo tee", category="merchandise", price=25.00, cost=8.50, is_available=True, allergens=[], dietary_tags=[], is_kids_friendly=False, popularity=70),
    ]
    db.add_all(menu_items)

    # 10. Inventory Items
    inventory_items = [
        InventoryItem(id=_id("inv-1"), name="2-Row Pale Malt", category="grain", current_stock=1800, unit="lbs", par_level=2000, reorder_point=500, cost_per_unit=0.65, supplier="Briess", location="Grain Room"),
        InventoryItem(id=_id("inv-2"), name="Crystal 60 Malt", category="grain", current_stock=350, unit="lbs", par_level=400, reorder_point=100, cost_per_unit=0.85, supplier="Briess", location="Grain Room"),
        InventoryItem(id=_id("inv-3"), name="Citra Hops", category="hops", current_stock=25, unit="lbs", par_level=30, reorder_point=8, cost_per_unit=18.50, supplier="Yakima Chief", location="Hop Freezer"),
        InventoryItem(id=_id("inv-4"), name="Mosaic Hops", category="hops", current_stock=18, unit="lbs", par_level=25, reorder_point=6, cost_per_unit=19.00, supplier="Yakima Chief", location="Hop Freezer"),
        InventoryItem(id=_id("inv-5"), name="US-05 Yeast", category="yeast", current_stock=22, unit="packets", par_level=30, reorder_point=10, cost_per_unit=4.50, supplier="Fermentis", location="Yeast Fridge"),
        InventoryItem(id=_id("inv-6"), name="PBW Cleaner", category="chemical", current_stock=15, unit="lbs", par_level=25, reorder_point=5, cost_per_unit=3.20, supplier="Five Star", location="Chemical Storage"),
        InventoryItem(id=_id("inv-7"), name="Star San", category="chemical", current_stock=6, unit="gal", par_level=10, reorder_point=2, cost_per_unit=12.50, supplier="Five Star", location="Chemical Storage"),
        InventoryItem(id=_id("inv-8"), name="16oz Crowler Cans", category="packaging", current_stock=2400, unit="units", par_level=5000, reorder_point=1000, cost_per_unit=0.35, supplier="Ball Corp", location="Packaging Area"),
        InventoryItem(id=_id("inv-9"), name="Angus Burger Patties", category="food", current_stock=180, unit="units", par_level=300, reorder_point=80, cost_per_unit=1.80, supplier="Sysco", location="Walk-in Cooler"),
        InventoryItem(id=_id("inv-10"), name="Chicken Wings", category="food", current_stock=45, unit="lbs", par_level=60, reorder_point=15, cost_per_unit=3.20, supplier="US Foods", location="Walk-in Cooler"),
        InventoryItem(id=_id("inv-11"), name="BH Logo T-Shirts", category="merchandise", current_stock=65, unit="units", par_level=100, reorder_point=20, cost_per_unit=8.50, supplier="Custom Ink", location="Merch Display"),
    ]
    db.add_all(inventory_items)

    # 11. Staff Members
    staff_members = [
        StaffMember(id=_id("staff-1"), first_name="Mike", last_name="Rodriguez", role="brewer", email="mike@beardedhop.com", phone="(830) 555-1001", hire_date="2025-03-15", hourly_rate=28.00, status="active", tabc_certified=True, tabc_expiry="2027-03-15", food_handler_certified=True, food_handler_expiry="2027-03-15", hours_this_week=42, sales_this_week=0, schedule=[{"day": "Mon", "startTime": "6:00 AM", "endTime": "2:00 PM", "role": "brewer"}]),
        StaffMember(id=_id("staff-2"), first_name="Jessica", last_name="Tran", role="bartender", email="jessica@beardedhop.com", phone="(830) 555-1002", hire_date="2025-06-01", hourly_rate=15.00, status="active", tabc_certified=True, tabc_expiry="2027-06-01", food_handler_certified=True, food_handler_expiry="2027-06-01", hours_this_week=35, sales_this_week=2450, schedule=[]),
        StaffMember(id=_id("staff-3"), first_name="Tony", last_name="Barboza", role="cook", email="tony@beardedhop.com", phone="(830) 555-1003", hire_date="2025-04-20", hourly_rate=18.00, status="active", tabc_certified=False, food_handler_certified=True, food_handler_expiry="2027-04-20", hours_this_week=38, sales_this_week=0, schedule=[]),
        StaffMember(id=_id("staff-4"), first_name="Amy", last_name="Nguyen", role="server", email="amy@beardedhop.com", phone="(830) 555-1004", hire_date="2025-08-15", hourly_rate=12.00, status="active", tabc_certified=True, tabc_expiry="2027-08-15", food_handler_certified=True, food_handler_expiry="2027-08-15", hours_this_week=30, sales_this_week=1890, schedule=[]),
        StaffMember(id=_id("staff-5"), first_name="David", last_name="Kim", role="manager", email="david@beardedhop.com", phone="(830) 555-1005", hire_date="2025-02-01", hourly_rate=32.00, status="active", tabc_certified=True, tabc_expiry="2027-02-01", food_handler_certified=True, food_handler_expiry="2027-02-01", hours_this_week=45, sales_this_week=0, schedule=[]),
        StaffMember(id=_id("staff-6"), first_name="Rachel", last_name="Kim", role="bartender", email="rachel@beardedhop.com", phone="(830) 555-1006", hire_date="2025-09-10", hourly_rate=15.00, status="active", tabc_certified=True, tabc_expiry="2027-09-10", food_handler_certified=True, food_handler_expiry="2027-09-10", hours_this_week=32, sales_this_week=2180, schedule=[]),
    ]
    db.add_all(staff_members)

    # 12. Wholesale Accounts
    wholesale_accounts = [
        WholesaleAccount(id=_id("wholesale-1"), business_name="The Rusty Tap", contact_name="Jim Rawlings", email="jim@rustytap.com", phone="(512) 555-3001", address="456 6th Street, Austin, TX", type="bar", status="active", total_orders=15, total_revenue=4850, kegs_out=4, credit_limit=5000, payment_terms="Net 30", notes="Our biggest wholesale account", taps_carrying=["Hill Country Haze", "Bulverde Blonde", "Lone Star Lager"]),
        WholesaleAccount(id=_id("wholesale-2"), business_name="Gruene General Store", contact_name="Martha Gruene", email="martha@gruenegeneral.com", phone="(830) 555-3002", address="1281 Gruene Rd, New Braunfels, TX", type="bottle-shop", status="active", total_orders=12, total_revenue=2890, kegs_out=6, credit_limit=3000, payment_terms="Net 15", notes="Great tourist traffic", taps_carrying=["Bulverde Blonde", "Hill Country Haze", "Prickly Pear Sour"]),
        WholesaleAccount(id=_id("wholesale-3"), business_name="Canyon Lake BBQ", contact_name="Hank Williams", email="hank@canyonlakebbq.com", phone="(830) 555-3003", address="789 Canyon Lake Dr, Canyon Lake, TX", type="restaurant", status="active", total_orders=8, total_revenue=1890, kegs_out=2, credit_limit=2500, payment_terms="Net 30", notes="BBQ pairs great with our porter", taps_carrying=["Mesquite Smoked Porter", "Lone Star Lager"]),
        WholesaleAccount(id=_id("wholesale-4"), business_name="Hill Country Market", contact_name="Patricia Hill", email="patricia@hcmarket.com", phone="(830) 555-3004", address="321 Main Plaza, Boerne, TX", type="grocery", status="prospect", total_orders=0, total_revenue=0, kegs_out=0, credit_limit=2000, payment_terms="Net 30", notes="Initial meeting scheduled", taps_carrying=[]),
    ]
    db.add_all(wholesale_accounts)

    # 13. Mug Club Members
    mug_club_members = [
        MugClubMember(id=_id("mc-1"), customer_id=_id("customer-1"), customer_name="Jake Morrison", tier="Premium", member_since="2026-01-15", renewal_date="2027-01-15", mug_number=7, mug_location="Rack A", total_saved=142.50, visits_as_member=24, referrals=3, status="active", benefits=["20oz pour for pint price", "10% food discount", "Exclusive tastings", "Birthday pint free"]),
        MugClubMember(id=_id("mc-2"), customer_id=_id("customer-2"), customer_name="Maria Gonzalez", tier="Standard", member_since="2026-02-01", renewal_date="2027-02-01", mug_number=12, mug_location="Rack B", total_saved=68.00, visits_as_member=16, referrals=1, status="active", benefits=["20oz pour for pint price", "5% food discount"]),
        MugClubMember(id=_id("mc-3"), customer_id=_id("customer-5"), customer_name="Bobby Whitfield", tier="Founding", member_since="2025-12-01", renewal_date="2026-12-01", mug_number=1, mug_location="Rack A - Top Shelf", total_saved=385.00, visits_as_member=32, referrals=5, status="active", benefits=["20oz pour for pint price", "15% food discount", "Exclusive tastings", "Birthday pint free", "Early release access", "Free growler fills monthly"]),
        MugClubMember(id=_id("mc-4"), customer_id=_id("customer-3"), customer_name="Tom Henderson", tier="Standard", member_since="2026-01-20", renewal_date="2027-01-20", mug_number=9, mug_location="Rack A", total_saved=95.00, visits_as_member=20, referrals=2, status="active", benefits=["20oz pour for pint price", "5% food discount"]),
    ]
    db.add_all(mug_club_members)

    # 14. Email Campaigns
    email_campaigns = [
        EmailCampaign(id=_id("camp-1"), name="March Beer Release", subject="Spring Saison Coming 3/15!", status="scheduled", segment="All Subscribers", scheduled_date="2026-03-12", recipients=450, opened=0, clicked=0, unsubscribed=0, type="new-release"),
        EmailCampaign(id=_id("camp-2"), name="Mug Club Exclusive Tasting", subject="Members Only: Spring Saison Pre-Release", status="sent", segment="Mug Club Members", sent_date="2026-03-01", recipients=41, opened=35, clicked=28, unsubscribed=0, type="mug-club"),
        EmailCampaign(id=_id("camp-3"), name="March Events Newsletter", subject="What's Happening at Bearded Hop", status="sent", segment="All Subscribers", sent_date="2026-03-03", recipients=450, opened=198, clicked=87, unsubscribed=2, type="newsletter"),
        EmailCampaign(id=_id("camp-4"), name="Happy Hour Promo", subject="Happy Hour M-F 3-6pm — $1 Off Pints!", status="sent", segment="Weekend Warriors", sent_date="2026-02-24", recipients=67, opened=42, clicked=18, unsubscribed=1, type="promotion"),
        EmailCampaign(id=_id("camp-5"), name="Birthday Club", subject="Happy Birthday! Free Pint Awaits", status="draft", segment="March Birthdays", recipients=12, opened=0, clicked=0, unsubscribed=0, type="birthday"),
    ]
    db.add_all(email_campaigns)

    # 15. Daily Sales (30 days)
    daily_sales = []
    for i in range(30):
        day = 3 + i  # Feb 3 to Mar 4
        month = 2 if day <= 28 else 3
        d = day if month == 2 else day - 28
        date_str = f"2026-{month:02d}-{d:02d}"
        base_beer = 3200 + (i * 47) % 800
        base_food = 1800 + (i * 31) % 600
        base_na = 280 + (i * 13) % 120
        base_merch = 120 + (i * 7) % 80
        base_event = 200 if i % 7 in (4, 5) else 0
        total = base_beer + base_food + base_na + base_merch + base_event
        count = 85 + (i * 3) % 40
        daily_sales.append(DailySales(
            id=_id(f"ds-{i}"), date=date_str, beer_revenue=base_beer, food_revenue=base_food,
            na_revenue=base_na, merchandise_revenue=base_merch, event_revenue=base_event,
            total_revenue=total, customer_count=count, avg_ticket=round(total / count, 2),
        ))
    db.add_all(daily_sales)

    # 16. Monthly Financials
    monthly_financials = [
        MonthlyFinancial(id=_id("mf-1"), month="2025-10", month_label="Oct", beer_revenue=42000, food_revenue=18500, na_revenue=3200, merchandise_revenue=1800, event_revenue=4500, wholesale_revenue=5200, total_revenue=75200, cogs=22560, labor_cost=18800, rent=4500, utilities=1200, marketing=800, insurance=600, licenses=100, supplies=400, misc=300, total_expenses=49260, net_profit=25940, net_margin_pct=34.5),
        MonthlyFinancial(id=_id("mf-2"), month="2025-11", month_label="Nov", beer_revenue=45000, food_revenue=20000, na_revenue=3500, merchandise_revenue=2200, event_revenue=5200, wholesale_revenue=5800, total_revenue=81700, cogs=24510, labor_cost=20425, rent=4500, utilities=1100, marketing=1200, insurance=600, licenses=100, supplies=450, misc=350, total_expenses=53235, net_profit=28465, net_margin_pct=34.8),
        MonthlyFinancial(id=_id("mf-3"), month="2025-12", month_label="Dec", beer_revenue=52000, food_revenue=23000, na_revenue=4200, merchandise_revenue=3800, event_revenue=8500, wholesale_revenue=6500, total_revenue=98000, cogs=29400, labor_cost=24500, rent=4500, utilities=1300, marketing=1500, insurance=600, licenses=100, supplies=500, misc=400, total_expenses=62800, net_profit=35200, net_margin_pct=35.9),
        MonthlyFinancial(id=_id("mf-4"), month="2026-01", month_label="Jan", beer_revenue=38000, food_revenue=16000, na_revenue=2800, merchandise_revenue=1500, event_revenue=3200, wholesale_revenue=4800, total_revenue=66300, cogs=19890, labor_cost=16575, rent=4500, utilities=1100, marketing=600, insurance=600, licenses=100, supplies=350, misc=250, total_expenses=43965, net_profit=22335, net_margin_pct=33.7),
        MonthlyFinancial(id=_id("mf-5"), month="2026-02", month_label="Feb", beer_revenue=44000, food_revenue=19500, na_revenue=3400, merchandise_revenue=2000, event_revenue=4800, wholesale_revenue=5500, total_revenue=79200, cogs=23760, labor_cost=19800, rent=4500, utilities=1150, marketing=900, insurance=600, licenses=100, supplies=400, misc=300, total_expenses=51510, net_profit=27690, net_margin_pct=35.0),
        MonthlyFinancial(id=_id("mf-6"), month="2026-03", month_label="Mar", beer_revenue=28000, food_revenue=12500, na_revenue=2100, merchandise_revenue=1200, event_revenue=3000, wholesale_revenue=3500, total_revenue=50300, cogs=15090, labor_cost=12575, rent=4500, utilities=1100, marketing=700, insurance=600, licenses=100, supplies=300, misc=200, total_expenses=35165, net_profit=15135, net_margin_pct=30.1),
    ]
    db.add_all(monthly_financials)

    # 17. TTB Reports
    ttb_reports = [
        TTBReport(id=_id("ttb-1"), month="2025-10", beginning_inventory=28, produced=42, received=0, transferred_taproom=35, transferred_distribution=8, ending_inventory=27, losses=0, excise_tax=147),
        TTBReport(id=_id("ttb-2"), month="2025-11", beginning_inventory=27, produced=49, received=0, transferred_taproom=38, transferred_distribution=10, ending_inventory=28, losses=0, excise_tax=171.5),
        TTBReport(id=_id("ttb-3"), month="2025-12", beginning_inventory=28, produced=56, received=0, transferred_taproom=42, transferred_distribution=12, ending_inventory=30, losses=0, excise_tax=196),
        TTBReport(id=_id("ttb-4"), month="2026-01", beginning_inventory=30, produced=49, received=0, transferred_taproom=40, transferred_distribution=10, ending_inventory=29, losses=0, excise_tax=171.5),
        TTBReport(id=_id("ttb-5"), month="2026-02", beginning_inventory=29, produced=56, received=0, transferred_taproom=44, transferred_distribution=14, ending_inventory=27, losses=0, excise_tax=196),
        TTBReport(id=_id("ttb-6"), month="2026-03", beginning_inventory=27, produced=35, received=0, transferred_taproom=28, transferred_distribution=8, ending_inventory=26, losses=0, excise_tax=122.5),
    ]
    db.add_all(ttb_reports)

    # 18. Compliance Items
    compliance_items = [
        ComplianceItem(id=_id("comp-1"), type="tabc", name="TABC Manufacturer License", status="compliant", due_date="2027-04-15", last_completed="2025-04-15", notes=""),
        ComplianceItem(id=_id("comp-2"), type="ttb", name="TTB Brewer's Notice", status="compliant", due_date="2027-03-01", last_completed="2025-03-01", notes=""),
        ComplianceItem(id=_id("comp-3"), type="health", name="Health Department Inspection", status="due-soon", due_date="2026-03-15", last_completed="2025-09-15", notes="Semi-annual inspection"),
        ComplianceItem(id=_id("comp-4"), type="music-license", name="BMI Music License", status="compliant", due_date="2027-01-01", last_completed="2026-01-01", notes=""),
        ComplianceItem(id=_id("comp-5"), type="business", name="City Business Permit", status="compliant", due_date="2027-06-30", last_completed="2025-06-30", notes=""),
    ]
    db.add_all(compliance_items)

    # 19. Social Metrics (30 days)
    social_metrics = []
    for i in range(30):
        day = 3 + i
        month = 2 if day <= 28 else 3
        d = day if month == 2 else day - 28
        social_metrics.append(SocialMetrics(
            id=_id(f"sm-{i}"), date=f"2026-{month:02d}-{d:02d}",
            instagram_followers=2680 + i * 5, facebook_likes=1380 + i * 2,
            untappd_checkins=8100 + i * 6, google_review_count=182 + i // 5,
            google_rating=4.6, instagram_engagement=round(2.8 + (i % 10) * 0.15, 1),
            facebook_engagement=round(1.4 + (i % 8) * 0.1, 1),
        ))
    db.add_all(social_metrics)

    # 20. Content Calendar
    content_cal = [
        ContentCalendar(id=_id("cc-1"), date="2026-03-05", platform="instagram", caption="Thirsty Thursday vibes. Hill Country Haze on tap.", status="posted", type="photo"),
        ContentCalendar(id=_id("cc-2"), date="2026-03-05", platform="facebook", caption="TONIGHT: Trivia Tuesday winners got a $50 gift card!", status="posted", type="photo"),
        ContentCalendar(id=_id("cc-3"), date="2026-03-06", platform="instagram", caption="Friday vibes start early. Live music tonight!", status="planned", type="reel"),
        ContentCalendar(id=_id("cc-4"), date="2026-03-06", platform="tiktok", caption="POV: The brewer walks you through brew day at Bearded Hop", status="planned", type="video"),
        ContentCalendar(id=_id("cc-5"), date="2026-03-07", platform="instagram", caption="Saturday at the brewery. Bring the whole family.", status="planned", type="story"),
        ContentCalendar(id=_id("cc-6"), date="2026-03-07", platform="facebook", caption="Kids Craft & Brew Saturday — 11am-3pm!", status="planned", type="photo"),
        ContentCalendar(id=_id("cc-7"), date="2026-03-08", platform="instagram", caption="Sunday funday. Brunch + brews + live music.", status="planned", type="photo"),
        ContentCalendar(id=_id("cc-8"), date="2026-03-08", platform="untappd", caption="New badge unlocked! Check in to our Spring Saison.", status="planned", type="checkin"),
        ContentCalendar(id=_id("cc-9"), date="2026-03-09", platform="instagram", caption="Monday vibes. Happy hour 3-6pm.", status="planned", type="photo"),
        ContentCalendar(id=_id("cc-10"), date="2026-03-10", platform="instagram", caption="Taco Tuesday + our Lone Star Lager = perfection", status="planned", type="reel"),
        ContentCalendar(id=_id("cc-11"), date="2026-03-10", platform="facebook", caption="Mug Club exclusive: Spring Saison pre-release tasting 3/13!", status="planned", type="photo"),
        ContentCalendar(id=_id("cc-12"), date="2026-03-11", platform="instagram", caption="Behind the scenes: Tony smoking brisket for 14 hours", status="planned", type="video"),
    ]
    db.add_all(content_cal)

    # 21. Customer Segments
    segments = [
        CustomerSegment(id=_id("seg-1"), name="IPA Lovers", count=45, avg_spend=68.50, visit_frequency="2.3x/month", top_beer="Hill Country Haze", suggested_campaign="New hop variety tasting invite", color="#f59e0b"),
        CustomerSegment(id=_id("seg-2"), name="Lager Loyalists", count=23, avg_spend=52.00, visit_frequency="1.8x/month", top_beer="Lone Star Lager", suggested_campaign="Mexican Lager & taco pairing night", color="#3b82f6"),
        CustomerSegment(id=_id("seg-3"), name="Weekend Warriors", count=67, avg_spend=74.20, visit_frequency="3.1x/month", top_beer="Bulverde Blonde", suggested_campaign="Happy hour weekday conversion offer", color="#10b981"),
        CustomerSegment(id=_id("seg-4"), name="Mug Club Members", count=28, avg_spend=89.00, visit_frequency="4.2x/month", top_beer="Barrel-Aged Imperial Stout", suggested_campaign="Exclusive member-only barrel tapping", color="#8b5cf6"),
        CustomerSegment(id=_id("seg-5"), name="Families", count=34, avg_spend=95.50, visit_frequency="1.5x/month", top_beer="Texas Sunset Wheat", suggested_campaign="Saturday kids event series", color="#ec4899"),
        CustomerSegment(id=_id("seg-6"), name="Event Regulars", count=19, avg_spend=62.00, visit_frequency="2.1x/month", top_beer="Prickly Pear Sour", suggested_campaign="Early-bird event ticket access", color="#f97316"),
        CustomerSegment(id=_id("seg-7"), name="New Visitors (30 days)", count=41, avg_spend=45.00, visit_frequency="1.0x/month", top_beer="Bulverde Blonde", suggested_campaign="Welcome back 10% off 2nd visit", color="#6b7280"),
    ]
    db.add_all(segments)

    # 22. Business Settings
    settings = BusinessSettings(
        id=_id("settings"), business_name="Bearded Hop Brewery",
        address="123 Main Street, Bulverde, TX 78163", phone="(830) 555-BREW",
        email="hello@beardedhopbrewery.com", tax_rate="8.25%",
        timezone="America/Chicago (CST)", currency="USD",
    )
    db.add(settings)

    # 23. Open Tabs
    open_tabs = [
        OpenTab(id=_id("tab-1"), customer_name="Jake Morrison", customer_id=_id("customer-1"), items=[{"name": "Hill Country Haze", "size": "Mug Club 20oz", "price": 7, "qty": 2}, {"name": "Smoked Wings (8pc)", "size": "", "price": 14.99, "qty": 1}, {"name": "Loaded Nachos", "size": "", "price": 12.99, "qty": 1}], opened_at="2026-03-05T17:15:00", server="Jessica Tran", subtotal=41.98, table_number="T-12"),
        OpenTab(id=_id("tab-2"), customer_name="Walk-in", items=[{"name": "Lone Star Lager", "size": "Pint", "price": 7, "qty": 2}, {"name": "Topo Chico", "size": "", "price": 4, "qty": 1}], opened_at="2026-03-05T18:30:00", server="Amy Nguyen", subtotal=18, table_number="P-5"),
        OpenTab(id=_id("tab-3"), customer_name="Carlos Rivera", customer_id=_id("customer-7"), items=[{"name": "Mesquite Smoked Porter", "size": "Pint", "price": 7, "qty": 1}, {"name": "Jalapeño Cream Ale", "size": "Half", "price": 5, "qty": 1}, {"name": "Brewhouse Burger", "size": "", "price": 16.99, "qty": 1}, {"name": "Loaded Fries", "size": "", "price": 8.99, "qty": 1}], opened_at="2026-03-05T18:05:00", server="Jessica Tran", subtotal=37.98),
        OpenTab(id=_id("tab-4"), customer_name="Bobby Whitfield", customer_id=_id("customer-5"), items=[{"name": "Barrel-Aged Imperial Stout", "size": "Mug Club 20oz", "price": 7, "qty": 1}, {"name": "Hill Country Haze", "size": "Mug Club 20oz", "price": 7, "qty": 1}, {"name": "Smoked Brisket Plate", "size": "", "price": 19.99, "qty": 1}, {"name": "Stout Brownie Sundae", "size": "", "price": 10.99, "qty": 1}, {"name": "Prickly Pear Sour", "size": "Mug Club 20oz", "price": 7, "qty": 1}, {"name": "BBQ Pulled Pork Sandwich", "size": "", "price": 14.99, "qty": 1}], opened_at="2026-03-05T16:00:00", server="Rachel Kim", subtotal=66.97, table_number="T-1"),
        OpenTab(id=_id("tab-5"), customer_name="Walk-in (Patio)", items=[{"name": "Bulverde Blonde", "size": "Pint", "price": 7, "qty": 3}, {"name": "Lavender Lemonade", "size": "", "price": 5.99, "qty": 2}, {"name": "Kids Chicken Tenders", "size": "", "price": 8.99, "qty": 2}], opened_at="2026-03-05T17:45:00", server="Amy Nguyen", subtotal=50.97, table_number="P-8"),
        OpenTab(id=_id("tab-6"), customer_name="Maria Gonzalez", customer_id=_id("customer-2"), items=[{"name": "Texas Sunset Wheat", "size": "Pint", "price": 7, "qty": 1}, {"name": "Fish Tacos", "size": "", "price": 15.99, "qty": 1}], opened_at="2026-03-05T18:40:00", server="Jessica Tran", subtotal=22.99),
        OpenTab(id=_id("tab-7"), customer_name="Tom Henderson", customer_id=_id("customer-3"), items=[{"name": "Lone Star Lager", "size": "Pint", "price": 7, "qty": 4}, {"name": "Loaded Nachos", "size": "", "price": 12.99, "qty": 2}, {"name": "Smoked Wings (8pc)", "size": "", "price": 14.99, "qty": 2}], opened_at="2026-03-05T19:10:00", server="Rachel Kim", subtotal=83.96),
    ]
    db.add_all(open_tabs)

    # 24. POS Transactions (last 20)
    pos_txns = [
        POSTransaction(id=_id("tx-1"), customer_name="Walk-in", items=[{"name": "Bulverde Blonde", "size": "Pint", "price": 7, "qty": 2}], subtotal=14, tax=1.16, total=15.16, payment_method="card", server="Jessica Tran", closed_at="2026-03-05T14:22:00", tip_amount=3),
        POSTransaction(id=_id("tx-2"), customer_name="Ashley Chen", items=[{"name": "Craft Root Beer", "size": "Large", "price": 6, "qty": 1}, {"name": "Kids Mac & Cheese", "size": "", "price": 7.99, "qty": 1}], subtotal=13.99, tax=1.15, total=15.14, payment_method="card", server="Amy Nguyen", closed_at="2026-03-05T14:45:00", tip_amount=3),
        POSTransaction(id=_id("tx-3"), customer_name="Walk-in", items=[{"name": "Hill Country Haze", "size": "Taster", "price": 3, "qty": 3}, {"name": "Prickly Pear Sour", "size": "Taster", "price": 3, "qty": 2}, {"name": "Citra Smash IPA", "size": "Taster", "price": 3, "qty": 1}], subtotal=18, tax=1.49, total=19.49, payment_method="cash", server="Rachel Kim", closed_at="2026-03-05T15:10:00"),
        POSTransaction(id=_id("tx-4"), customer_name="Diane Foster", items=[{"name": "Texas Sunset Wheat", "size": "Pint", "price": 7, "qty": 1}], subtotal=49.94, tax=4.12, total=54.06, payment_method="card", server="Amy Nguyen", closed_at="2026-03-05T15:30:00", tip_amount=10),
        POSTransaction(id=_id("tx-5"), customer_name="Jake Morrison", items=[{"name": "Hill Country Haze", "size": "Mug Club 20oz", "price": 7, "qty": 2}, {"name": "Brewhouse Burger", "size": "", "price": 16.99, "qty": 1}], subtotal=30.99, tax=2.56, total=33.55, payment_method="mug-club", server="Jessica Tran", closed_at="2026-03-05T13:15:00", tip_amount=7),
        POSTransaction(id=_id("tx-6"), customer_name="Walk-in", items=[{"name": "Barrel-Aged Imperial Stout", "size": "Half", "price": 5, "qty": 2}], subtotal=23.99, tax=1.98, total=25.97, payment_method="card", server="Rachel Kim", closed_at="2026-03-05T15:50:00", tip_amount=5),
        POSTransaction(id=_id("tx-7"), customer_name="Walk-in", items=[{"name": "Lone Star Lager", "size": "Pint", "price": 7, "qty": 1}], subtotal=7, tax=0.58, total=7.58, payment_method="cash", server="Amy Nguyen", closed_at="2026-03-05T16:05:00"),
        POSTransaction(id=_id("tx-8"), customer_name="Linda Thompson", items=[{"name": "Craft Root Beer", "size": "Large", "price": 6, "qty": 1}], subtotal=25.99, tax=2.14, total=28.13, payment_method="card", server="Jessica Tran", closed_at="2026-03-05T16:20:00", tip_amount=5),
        POSTransaction(id=_id("tx-9"), customer_name="Walk-in", items=[{"name": "BH Logo T-Shirt", "size": "L", "price": 25, "qty": 1}], subtotal=41, tax=3.38, total=44.38, payment_method="card", server="Rachel Kim", closed_at="2026-03-05T16:45:00"),
        POSTransaction(id=_id("tx-10"), customer_name="Walk-in", items=[{"name": "Citra Smash IPA", "size": "Pint", "price": 7, "qty": 2}], subtotal=25.99, tax=2.14, total=28.13, payment_method="card", server="Amy Nguyen", closed_at="2026-03-05T17:00:00", tip_amount=5),
    ]
    db.add_all(pos_txns)

    # 25. Floor Tables (26 tables across 5 zones)
    floor_tables = [
        # Taproom
        FloorTable(id="T-1", zone="taproom", label="T1", seats=4, x=220, y=180, shape="rect", width=48, height=48, status="occupied", current_tab_id=str(_id("tab-4")), current_customer_name="Bobby Whitfield", current_customer_id=str(_id("customer-5")), party_size=2, server_id=str(_id("staff-6")), server_name="Rachel Kim", seated_at="2026-03-05T16:00:00"),
        FloorTable(id="T-2", zone="taproom", label="T2", seats=2, x=310, y=160, shape="circle", radius=22, status="available"),
        FloorTable(id="T-3", zone="taproom", label="T3", seats=4, x=400, y=180, shape="rect", width=48, height=48, status="occupied", current_tab_id=str(_id("tab-3")), current_customer_name="Carlos Rivera", current_customer_id=str(_id("customer-7")), party_size=2, server_id=str(_id("staff-2")), server_name="Jessica Tran", seated_at="2026-03-05T18:05:00"),
        FloorTable(id="T-4", zone="taproom", label="T4", seats=2, x=220, y=270, shape="circle", radius=22, status="reserved", reservation_id=str(_id("res-1"))),
        FloorTable(id="T-5", zone="taproom", label="T5", seats=4, x=310, y=260, shape="rect", width=48, height=48, status="occupied", current_tab_id=str(_id("tab-6")), current_customer_name="Maria Gonzalez", current_customer_id=str(_id("customer-2")), party_size=2, server_id=str(_id("staff-2")), server_name="Jessica Tran", seated_at="2026-03-05T18:40:00"),
        FloorTable(id="T-6", zone="taproom", label="T6", seats=2, x=400, y=280, shape="circle", radius=22, status="available"),
        FloorTable(id="T-7", zone="taproom", label="T7", seats=4, x=310, y=350, shape="rect", width=48, height=48, status="needs-attention", current_customer_name="Walk-in", party_size=3, server_id=str(_id("staff-4")), server_name="Amy Nguyen", seated_at="2026-03-05T17:15:00"),
        FloorTable(id="T-8", zone="taproom", label="T8", seats=8, x=460, y=260, shape="community", width=80, height=40, status="occupied", current_tab_id=str(_id("tab-7")), current_customer_name="Tom Henderson", current_customer_id=str(_id("customer-3")), party_size=6, server_id=str(_id("staff-6")), server_name="Rachel Kim", seated_at="2026-03-05T19:10:00"),
        # Bar
        FloorTable(id="B-1", zone="bar", label="B1", seats=1, x=180, y=55, shape="circle", radius=16, status="occupied", current_tab_id=str(_id("tab-1")), current_customer_name="Jake Morrison", current_customer_id=str(_id("customer-1")), party_size=1, server_id=str(_id("staff-2")), server_name="Jessica Tran", seated_at="2026-03-05T17:15:00"),
        FloorTable(id="B-2", zone="bar", label="B2", seats=1, x=240, y=55, shape="circle", radius=16, status="available"),
        FloorTable(id="B-3", zone="bar", label="B3", seats=1, x=300, y=55, shape="circle", radius=16, status="occupied", current_customer_name="Walk-in", party_size=1, server_id=str(_id("staff-6")), server_name="Rachel Kim", seated_at="2026-03-05T18:50:00"),
        FloorTable(id="B-4", zone="bar", label="B4", seats=1, x=360, y=55, shape="circle", radius=16, status="available"),
        FloorTable(id="B-5", zone="bar", label="B5", seats=1, x=420, y=55, shape="circle", radius=16, status="occupied", current_customer_name="Walk-in", party_size=2, server_id=str(_id("staff-2")), server_name="Jessica Tran", seated_at="2026-03-05T19:05:00"),
        FloorTable(id="B-6", zone="bar", label="B6", seats=1, x=480, y=55, shape="circle", radius=16, status="available"),
        # Patio
        FloorTable(id="P-1", zone="patio", label="P1", seats=4, x=640, y=160, shape="rect", width=48, height=48, status="available"),
        FloorTable(id="P-2", zone="patio", label="P2", seats=4, x=740, y=160, shape="rect", width=48, height=48, status="needs-attention", current_customer_name="Walk-in", party_size=4, server_id=str(_id("staff-4")), server_name="Amy Nguyen", seated_at="2026-03-05T17:30:00"),
        FloorTable(id="P-3", zone="patio", label="P3", seats=6, x=640, y=260, shape="rect", width=56, height=48, status="reserved", reservation_id=str(_id("res-2"))),
        FloorTable(id="P-4", zone="patio", label="P4", seats=4, x=740, y=260, shape="rect", width=48, height=48, status="occupied", current_tab_id=str(_id("tab-5")), current_customer_name="Walk-in (Patio)", party_size=5, server_id=str(_id("staff-4")), server_name="Amy Nguyen", seated_at="2026-03-05T17:45:00"),
        # Beer Garden
        FloorTable(id="G-1", zone="beer-garden", label="G1", seats=6, x=160, y=460, shape="rect", width=60, height=36, status="available"),
        FloorTable(id="G-2", zone="beer-garden", label="G2", seats=6, x=260, y=460, shape="rect", width=60, height=36, status="occupied", current_customer_name="Walk-in Group", party_size=8, server_id=str(_id("staff-4")), server_name="Amy Nguyen", seated_at="2026-03-05T18:20:00"),
        FloorTable(id="G-3", zone="beer-garden", label="G3", seats=6, x=360, y=460, shape="rect", width=60, height=36, status="available"),
        FloorTable(id="G-4", zone="beer-garden", label="G4", seats=6, x=160, y=530, shape="rect", width=60, height=36, status="available"),
        FloorTable(id="G-5", zone="beer-garden", label="G5", seats=6, x=260, y=530, shape="rect", width=60, height=36, status="occupied", current_customer_name="Walk-in Couple", party_size=2, server_id=str(_id("staff-6")), server_name="Rachel Kim", seated_at="2026-03-05T19:00:00"),
        FloorTable(id="G-6", zone="beer-garden", label="G6", seats=6, x=360, y=530, shape="rect", width=60, height=36, status="closed"),
        # Private Room
        FloorTable(id="R-1", zone="private-room", label="R1", seats=20, x=660, y=50, shape="rect", width=70, height=40, status="reserved", reservation_id=str(_id("res-3"))),
        FloorTable(id="R-2", zone="private-room", label="R2", seats=20, x=770, y=50, shape="rect", width=70, height=40, status="available"),
    ]
    db.add_all(floor_tables)

    # 26. Service Alerts
    service_alerts = [
        ServiceAlert(id=_id("alert-1"), table_id="T-7", type="no-order", message="Table T7 seated 45+ min with no food order", priority="high", created_at="2026-03-05T18:00:00"),
        ServiceAlert(id=_id("alert-2"), table_id="P-2", type="check-requested", message="Table P2 requested check", priority="medium", created_at="2026-03-05T18:25:00"),
        ServiceAlert(id=_id("alert-3"), table_id="T-8", type="high-tab", message="Table T8 tab exceeds $80 — verify party", priority="low", created_at="2026-03-05T19:15:00"),
        ServiceAlert(id=_id("alert-4"), table_id="T-1", type="long-seated", message="Table T1 occupied 3+ hours (Bobby Whitfield VIP)", priority="low", created_at="2026-03-05T19:00:00"),
        ServiceAlert(id=_id("alert-5"), table_id="T-4", type="reservation-due", message="Jake Morrison party of 4 arriving in 12 min (T4)", priority="medium", created_at="2026-03-05T19:18:00"),
        ServiceAlert(id=_id("alert-6"), table_id="B-5", type="long-seated", message="Bar B5 — 2 guests seated 55 min, only 1 drink ordered", priority="medium", created_at="2026-03-05T19:05:00"),
    ]
    db.add_all(service_alerts)

    # 27. Order Timelines
    order_timelines = [
        OrderTimeline(id=_id("ot-1"), table_id="T-1", time="2026-03-05T16:00:00", action="seated", description="Seated Bobby Whitfield, party of 2"),
        OrderTimeline(id=_id("ot-2"), table_id="T-1", time="2026-03-05T16:05:00", action="ordered", description="1x Barrel-Aged Imperial Stout (Mug Club 20oz)"),
        OrderTimeline(id=_id("ot-3"), table_id="T-1", time="2026-03-05T16:08:00", action="ordered", description="1x Hill Country Haze (Mug Club 20oz)"),
        OrderTimeline(id=_id("ot-4"), table_id="T-1", time="2026-03-05T16:15:00", action="ordered", description="1x Smoked Brisket Plate, 1x BBQ Pulled Pork Sandwich"),
        OrderTimeline(id=_id("ot-5"), table_id="T-1", time="2026-03-05T16:30:00", action="served", description="Food served to table"),
        OrderTimeline(id=_id("ot-6"), table_id="T-3", time="2026-03-05T18:05:00", action="seated", description="Seated Carlos Rivera, party of 2"),
        OrderTimeline(id=_id("ot-7"), table_id="T-3", time="2026-03-05T18:10:00", action="ordered", description="1x Mesquite Smoked Porter, 1x Jalapeño Cream Ale"),
        OrderTimeline(id=_id("ot-8"), table_id="T-3", time="2026-03-05T18:35:00", action="served", description="Food served to table"),
        OrderTimeline(id=_id("ot-9"), table_id="T-8", time="2026-03-05T19:10:00", action="seated", description="Seated Tom Henderson trivia group, party of 6"),
        OrderTimeline(id=_id("ot-10"), table_id="T-8", time="2026-03-05T19:15:00", action="ordered", description="4x Lone Star Lager, 2x Loaded Nachos, 2x Smoked Wings"),
        OrderTimeline(id=_id("ot-11"), table_id="P-4", time="2026-03-05T17:45:00", action="seated", description="Walk-in family party of 5"),
        OrderTimeline(id=_id("ot-12"), table_id="P-4", time="2026-03-05T17:50:00", action="ordered", description="3x Bulverde Blonde, 2x Lavender Lemonade"),
        OrderTimeline(id=_id("ot-13"), table_id="B-1", time="2026-03-05T17:15:00", action="seated", description="Jake Morrison seated at bar"),
        OrderTimeline(id=_id("ot-14"), table_id="B-1", time="2026-03-05T17:18:00", action="ordered", description="2x Hill Country Haze (Mug Club 20oz)"),
    ]
    db.add_all(order_timelines)

    # 28. Purchase Orders
    purchase_orders = [
        PurchaseOrder(id=_id("po-1"), po_number="PO-2026-041", supplier="Briess", items=[{"name": "2-Row Pale Malt", "qty": 2000, "unit": "lbs", "unitCost": 0.65}, {"name": "Crystal 60 Malt", "qty": 200, "unit": "lbs", "unitCost": 0.85}], total_cost=1470, status="received", order_date="2026-02-18", eta="2026-02-25", received_date="2026-02-24"),
        PurchaseOrder(id=_id("po-2"), po_number="PO-2026-042", supplier="Yakima Chief", items=[{"name": "Citra Hops", "qty": 30, "unit": "lbs", "unitCost": 18.50}, {"name": "Mosaic Hops", "qty": 25, "unit": "lbs", "unitCost": 19.00}], total_cost=1360, status="received", order_date="2026-02-12", eta="2026-02-20", received_date="2026-02-19"),
        PurchaseOrder(id=_id("po-3"), po_number="PO-2026-043", supplier="Fermentis", items=[{"name": "US-05 Yeast", "qty": 30, "unit": "packets", "unitCost": 4.50}], total_cost=225, status="received", order_date="2026-02-10", eta="2026-02-17", received_date="2026-02-16"),
        PurchaseOrder(id=_id("po-4"), po_number="PO-2026-044", supplier="Ball Corp", items=[{"name": "16oz Crowler Cans", "qty": 5000, "unit": "units", "unitCost": 0.35}], total_cost=1750, status="ordered", order_date="2026-03-01", eta="2026-03-10"),
        PurchaseOrder(id=_id("po-5"), po_number="PO-2026-045", supplier="US Foods", items=[{"name": "Beef Brisket", "qty": 80, "unit": "lbs", "unitCost": 4.50}, {"name": "Chicken Wings", "qty": 60, "unit": "lbs", "unitCost": 3.20}], total_cost=552, status="partial", order_date="2026-02-28", eta="2026-03-04", notes="Wings backordered"),
        PurchaseOrder(id=_id("po-6"), po_number="PO-2026-046", supplier="Sysco", items=[{"name": "Angus Burger Patties", "qty": 300, "unit": "units", "unitCost": 1.80}], total_cost=705, status="ordered", order_date="2026-03-02", eta="2026-03-06"),
    ]
    db.add_all(purchase_orders)

    # 29. Wholesale Orders
    wholesale_orders = [
        WholesaleOrder(id=_id("wo-1"), order_number="WO-2026-101", account_id=_id("wholesale-1"), account_name="The Rusty Tap", items=[{"beerName": "Hill Country Haze", "kegSize": "1/2", "quantity": 2, "unitPrice": 200}], total=590, status="delivered", order_date="2026-02-25", delivery_date="2026-02-28", payment_status="current"),
        WholesaleOrder(id=_id("wo-2"), order_number="WO-2026-102", account_id=_id("wholesale-2"), account_name="Gruene General Store", items=[{"beerName": "Bulverde Blonde", "kegSize": "1/6", "quantity": 4, "unitPrice": 80}], total=490, status="delivered", order_date="2026-02-20", delivery_date="2026-02-22", payment_status="current"),
        WholesaleOrder(id=_id("wo-3"), order_number="WO-2026-103", account_id=_id("wholesale-3"), account_name="Canyon Lake BBQ", items=[{"beerName": "Mesquite Smoked Porter", "kegSize": "1/2", "quantity": 1, "unitPrice": 210}], total=395, status="invoiced", order_date="2026-02-18", delivery_date="2026-02-20", payment_status="30-days"),
        WholesaleOrder(id=_id("wo-4"), order_number="WO-2026-104", account_id=_id("wholesale-1"), account_name="The Rusty Tap", items=[{"beerName": "Hill Country Haze", "kegSize": "1/2", "quantity": 2, "unitPrice": 200}], total=400, status="shipped", order_date="2026-03-03", delivery_date="2026-03-05", payment_status="current"),
        WholesaleOrder(id=_id("wo-5"), order_number="WO-2026-105", account_id=_id("wholesale-2"), account_name="Gruene General Store", items=[{"beerName": "Prickly Pear Sour", "kegSize": "1/6", "quantity": 3, "unitPrice": 85}], total=480, status="pending", order_date="2026-03-04", payment_status="current"),
    ]
    db.add_all(wholesale_orders)

    await db.commit()
