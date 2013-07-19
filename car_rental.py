import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

import netsvc
from osv import fields, osv
import tools
from tools.translate import _
import decimal_precision as dp


###################################
#This module to specify the color make

class car_make(osv.osv):
    _name='car.make'
    _description='this module to add a new car make'
    _columns={
              'name':fields.char('Car Make',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_make_id' , 'Car Make'),
                             
             }
car_make()  

###################################
#This module to specify the car brand

class car_brand(osv.osv):
    _name='car.brand'
    _description='this module to add a new car brand'
    _columns={
              'name':fields.char('Car Brand',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_brand_id' , 'Car Brand'),
               
             }
car_brand()  

    
###################################
#This module to specify the car brand class

class car_class(osv.osv):
    _name='car.class'
    _description='this module to add a new car class'
    _columns={
              'name':fields.char('Car Class',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_class_id' , 'Car Class'),
               
             }
car_class()  

###################################
#This module to specify the car brand class

class car_color(osv.osv):
    _name='car.color'
    _description='this module to add a new car color'
    _columns={
              'name':fields.char('Car Class',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_color_id' , 'Car Color'),
               
             }
car_color()  
        

class car_rental(osv.osv):
    _name='car.rental'
    _inherits = {'product.product': 'product_id'}
    #_inherit='product.product'
    _description='Module for Car Rental Management'
    _columns={
	          #'product_id': fields.many2one('res.partner', 'Partner'),
              'car_make_id': fields.many2one('car.make', 'Car Make'),
              'car_brand_id': fields.many2one('car.brand', 'Car Brand'),
              'car_class_id': fields.many2one('car.class', 'Car Class'),
              'car_color_id': fields.many2one('car.color', 'Car Color'),
              'cost':fields.float('Rent Cost',help='This fiels to determine the cost of rent per hour'),
              'rent_start_date': fields.date('Rent Start Date', required=True),
              'rent_end_date':fields.date('Rent End Date', required=True),
              #'rent_state':fields.selection([('cancelled','Cancelled'),('running','Running'),('finished','Finished')],'Rent State'),
              #'active':fields.boolean('Active'),
              'notes':fields.text('Details'),
              
              'name':fields.char('Vehicle Name',size=20,required=True),
              'regnno':fields.char('Vehicle Registration #',size=11,required=True),
              'company':fields.many2one('res.company','Company',required=True),
              'assetacc':fields.many2one('account.account',string='Asset Account',domain=[('type','=','vehicle')],required=True),
              'depracc':fields.many2one('account.account',string='Depreciation Account',required=True),
              'year':fields.char('Year',size=4),              
              'serial':fields.char('productSerial #',size=50),
              'type': fields.selection([
                         ('truck','Truck'),
                         ('bus','Bus'),
                         ('car','Car')], 'Class', required=True,),        
              'status': fields.selection([
                        ('active','Active'),
                        ('inactive','InActive'),
                        ('outofservice','Out of Service'),                        
                        ], 'status', required=True,),
              'ownership': fields.selection([
                        ('owned','Owned'),
                        ('leased','Leased'),
                        ('rented','Rented'),                       
                        ], 'Ownership', required=True),                 
              #'schedname':fields.many2one('fleet.service.templ','PM Schedule',help="Preventive maintainance schedule for this vehicle",required=True),
              'cmil':fields.float('Current Mileage',digits = (16,3)),
              'bmil':fields.float('Base Mileage',digits=(16,3),help="The last recorded mileage"),
              'bdate':fields.date('Recorded Date',help="Date on which the mileage is recorded"),
              'pdate':fields.date('Purchase Date',help="Date of Purchase of vehicle"),
              'pcost':fields.float('Purchase Value',digits=(16,2)),
              
              'ppartner':fields.many2one('res.partner','Purchased From'),
              
              'pinvoice':fields.char('Purchase Invoice',size=15),
              'podometer':fields.integer('Odometer at Purchase'),
              'startodometer':fields.integer('Start Odometer',required=True),
              #'lastodometer':fields.function(_lastodometer , method=True ,string='Last Odometer',digits=(11,0)),
              #'lastrecdate':fields.function(_lastododate , method=True , string='on date'),
              'deprecperc':fields.float('Depreciation in %',digits=(10,2),required=True),
              'deprecperd':fields.selection([
                                               ('monthly','Monthly'),
                                               ('quarterly','Quarterly'),
                                               ('halfyearly','Half Yearly'),
                                               ('annual','Yearly')
                                               ],'Depr. period',required=True),                
              'primarymeter':fields.selection([
                                                 ('odometer','Odometer'),
                                                 ('hourmeter','Hour Meter'),
                                                 ],'Primary Meter',required=True),
              'fueltype':fields.selection([
                                             ('hyrbrid','Hybrid'),
                                             ('diesel','Diesel'),
                                             ('gasoline','Gasoline'),
                                             ('cng','C.N.G'),
                                             ('lpg','L.P.G'),
                                             ('electric','Electric')
                                             ],'Fuel Used',required=True),
              #'fuelcardno':fields.one2one('fleet.fuelcards','Fuel Card #'),
              'fueltankcap':fields.float('Fuel Tank Capacity'),
              'warrexp':fields.date('Date',help="Expiry date for warranty of product"),
              'warrexpmil':fields.integer('(or) Mileage',help="Expiry mileage for warranty of product"),
              
              'location':fields.many2one('stock.location','Stk Location',help="Select the stock location or create one for each vehicle(recommended) so that the spares, tyres etc are assossiated with the vehicle when issued",required=True),
              
              }
    
    _defaults = {
        'rent_start_date': lambda *a: time.strftime('%Y-%m-01'),
        'rent_end_date': lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],
        'type':lambda *a:'vehicle',
        'status':lambda *a:'active',
        'ownership':lambda *a:'owned',
        'fueltype':lambda *a:'diesel',
        'primarymeter':lambda *a:'odometer',
        'deprecperd':lambda *a:'annual'
    }
    _sql_constraints = [
        ('uniq_regn_no', 'unique (regnno)', 'The registration no of the vehicle must be unique !')
    ]

car_rental()

