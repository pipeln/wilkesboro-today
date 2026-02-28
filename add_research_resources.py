#!/usr/bin/env python3
"""
Deep Research Agent - Add discovered resources to Supabase
This script adds government, healthcare, housing, food, and other community resources
discovered during deep research to the Wilkesboro.net Supabase database.
"""

import os
import sys
from datetime import datetime, timezone

# Add workspace to path
sys.path.insert(0, '/root/.openclaw/workspace')

from supabase_client import get_supabase, create_record

# Resources discovered during deep research
RESOURCES = [
    # GOVERNMENT RESOURCES - Wilkes County
    {
        "name": "Wilkes County Government",
        "type": "Government",
        "address": "110 North Street, Wilkesboro, NC 28697",
        "phone": "336-651-7300",
        "website": "https://wilkescounty.net",
        "description": "Official county government offices serving Wilkes County residents",
        "status": "Active",
        "tags": ["government", "county services"]
    },
    {
        "name": "Wilkes County Department of Social Services",
        "type": "Government",
        "address": "304 College St., Wilkesboro, NC 28697",
        "phone": "336-651-7400",
        "email": "",
        "website": "https://www.ncdhhs.gov/divisions/social-services/wilkes-county-department-social-services",
        "description": "Provides social services including food assistance, Medicaid, child protective services, and adult services",
        "status": "Active",
        "tags": ["social services", "DSS", "food assistance", "Medicaid", "child services"]
    },
    {
        "name": "Town of Wilkesboro",
        "type": "Government",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://wilkesboronc.org",
        "description": "Official town government for Wilkesboro, county seat of Wilkes County",
        "status": "Active",
        "tags": ["government", "municipal"]
    },
    {
        "name": "Wilkes County Veterans Services Office",
        "type": "Government",
        "address": "416 Executive Drive, Suite F, Wilkesboro, NC 28697",
        "phone": "336-570-6763",
        "website": "https://wilkescounty.net/244/Veterans-Services",
        "description": "Assists veterans with benefits claims, pension applications, and VA services",
        "status": "Active",
        "tags": ["veterans", "VA benefits", "military"]
    },
    {
        "name": "Wilkes County Board of Elections",
        "type": "Government",
        "address": "110 North Street, Wilkesboro, NC 28697",
        "phone": "336-651-7331",
        "website": "https://www.ncsbe.gov",
        "description": "Manages voter registration, elections, and voting information for Wilkes County",
        "status": "Active",
        "tags": ["elections", "voting", "civic"]
    },
    
    # GOVERNMENT RESOURCES - Surrounding Counties
    {
        "name": "Caldwell County Government",
        "type": "Government",
        "address": "905 West Avenue, Lenoir, NC 28645",
        "phone": "828-757-1300",
        "website": "https://www.caldwellcountync.org",
        "description": "Official county government serving Caldwell County including Lenoir, Granite Falls, and Hudson",
        "status": "Active",
        "tags": ["government", "county services", "Caldwell County"]
    },
    {
        "name": "Caldwell County Department of Social Services",
        "type": "Government",
        "address": "2345 Morganton Blvd., SW, Suite A, Lenoir, NC 28645",
        "phone": "828-426-8200",
        "email": "",
        "website": "https://www.ncdhhs.gov/divisions/social-services/caldwell-county-department-social-services",
        "description": "Social services for Caldwell County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Caldwell County"]
    },
    {
        "name": "Alexander County Government",
        "type": "Government",
        "address": "621 Liledoun Road, Taylorsville, NC 28681",
        "phone": "828-632-9332",
        "website": "https://alexandercountync.gov",
        "description": "Official county government serving Alexander County with county seat in Taylorsville",
        "status": "Active",
        "tags": ["government", "county services", "Alexander County"]
    },
    {
        "name": "Alexander County Department of Social Services",
        "type": "Government",
        "address": "604 7th St. SW, Taylorsville, NC 28681",
        "phone": "828-632-1080",
        "email": "",
        "website": "https://www.ncdhhs.gov/divisions/social-services/local-dss-directory/alexander-county-department-social-services",
        "description": "Social services for Alexander County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Alexander County"]
    },
    {
        "name": "Iredell County Government",
        "type": "Government",
        "address": "200 South Center Street, Statesville, NC 28677",
        "phone": "704-878-3000",
        "website": "https://www.iredellcountync.gov",
        "description": "Official county government serving Iredell County including Statesville and Mooresville",
        "status": "Active",
        "tags": ["government", "county services", "Iredell County"]
    },
    {
        "name": "Iredell County Department of Social Services",
        "type": "Government",
        "address": "549 Eastside Drive, Statesville, NC 28625",
        "phone": "704-873-5631",
        "website": "https://www.ncdhhs.gov/divisions/social-services/iredell-county-department-social-services",
        "description": "Social services for Iredell County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Iredell County"]
    },
    {
        "name": "Alleghany County Government",
        "type": "Government",
        "address": "348 South Main Street, PO Box 366, Sparta, NC 28675",
        "phone": "336-372-4179",
        "website": "https://alleghanycounty-nc.gov",
        "description": "Official county government serving Alleghany County with county seat in Sparta",
        "status": "Active",
        "tags": ["government", "county services", "Alleghany County"]
    },
    {
        "name": "Alleghany County Department of Social Services",
        "type": "Government",
        "address": "182 Doctors St., Sparta, NC 28675",
        "phone": "336-372-2411",
        "email": "",
        "website": "https://www.ncdhhs.gov/divisions/social-services/alleghany-county-department-social-services",
        "description": "Social services for Alleghany County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Alleghany County"]
    },
    {
        "name": "Ashe County Government",
        "type": "Government",
        "address": "150 Government Circle Suite 2500, Jefferson, NC 28640",
        "phone": "336-846-5501",
        "email": "administration@ashecountygov.com",
        "website": "https://www.ashecountygov.com",
        "description": "Official county government serving Ashe County including West Jefferson and Jefferson",
        "status": "Active",
        "tags": ["government", "county services", "Ashe County"]
    },
    {
        "name": "Surry County Government",
        "type": "Government",
        "address": "114 W. Atkins Street, PO Box 1467, Dobson, NC 27017",
        "phone": "",
        "website": "https://www.co.surry.nc.us",
        "description": "Official county government serving Surry County including Dobson, Elkin, Mount Airy, and Pilot Mountain",
        "status": "Active",
        "tags": ["government", "county services", "Surry County"]
    },
    {
        "name": "Surry County Department of Social Services",
        "type": "Government",
        "address": "118 Hamby Road, Dobson, NC 27017",
        "phone": "336-401-8700",
        "website": "https://www.ncdhhs.gov/divisions/social-services/surry-county-department-social-services",
        "description": "Social services for Surry County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Surry County"]
    },
    {
        "name": "Yadkin County Government",
        "type": "Government",
        "address": "217 East Willow Street, PO Box 220, Yadkinville, NC 27055",
        "phone": "336-849-7900",
        "website": "https://www.yadkincountync.gov",
        "description": "Official county government serving Yadkin County with county seat in Yadkinville",
        "status": "Active",
        "tags": ["government", "county services", "Yadkin County"]
    },
    {
        "name": "Yadkin County Human Services",
        "type": "Government",
        "address": "250 Willow St., Yadkinville, NC 27055",
        "phone": "336-849-7910",
        "website": "https://www.ncdhhs.gov/divisions/social-services/yadkin-county-human-services",
        "description": "Human services including social services for Yadkin County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Yadkin County"]
    },
    {
        "name": "Watauga County Government",
        "type": "Government",
        "address": "814 W King St, Boone, NC 28607",
        "phone": "",
        "website": "https://www.wataugacounty.org",
        "description": "Official county government serving Watauga County with county seat in Boone",
        "status": "Active",
        "tags": ["government", "county services", "Watauga County"]
    },
    {
        "name": "Watauga County Department of Social Services",
        "type": "Government",
        "address": "132 Poplar Grove Connector, Suite C, Boone, NC 28607",
        "phone": "828-265-8100",
        "website": "https://www.ncdhhs.gov/divisions/social-services/watauga-county-department-social-services",
        "description": "Social services for Watauga County residents",
        "status": "Active",
        "tags": ["social services", "DSS", "Watauga County"]
    },
    
    # HEALTHCARE RESOURCES
    {
        "name": "Wilkes Medical Center (Atrium Health Wake Forest Baptist)",
        "type": "Healthcare",
        "address": "1370 West D Street, North Wilkesboro, NC 28659",
        "phone": "336-651-8100",
        "website": "https://www.wakehealth.edu/locations/hospitals/wilkes-medical-center",
        "description": "Full-service hospital providing emergency care, surgical services, and comprehensive medical care",
        "status": "Active",
        "tags": ["hospital", "emergency", "healthcare"]
    },
    {
        "name": "Wilkes Community Health Center",
        "type": "Healthcare",
        "address": "Wilkes County",
        "phone": "",
        "website": "https://wilkescounty.net/567/Health-Center",
        "description": "Provides comprehensive primary and preventive care services to Wilkes and surrounding county residents of all ages",
        "status": "Active",
        "tags": ["healthcare", "primary care", "community health"]
    },
    {
        "name": "FastMed Urgent Care - Wilkesboro",
        "type": "Healthcare",
        "address": "Addison Ave, Wilkesboro, NC",
        "phone": "336-667-2710",
        "email": "",
        "website": "https://www.fastmed.com/urgent-care-centers/wilkesboro-nc-walk-in-clinic/",
        "description": "Walk-in urgent care clinic for non-emergency medical needs",
        "status": "Active",
        "tags": ["urgent care", "walk-in clinic", "healthcare"]
    },
    {
        "name": "Bethany Medical at North Wilkesboro",
        "type": "Healthcare",
        "address": "North Wilkesboro, NC",
        "phone": "",
        "website": "https://mybethanymedical.com/locations/bethany-medical-at-north-wilkesboro/",
        "description": "Primary care, urgent care, weight loss clinic, DOT physicals, pain management, and imaging services",
        "status": "Active",
        "tags": ["primary care", "urgent care", "healthcare"]
    },
    {
        "name": "Atrium Health Wake Forest Baptist Urgent Care - Wilkes",
        "type": "Healthcare",
        "address": "North Wilkesboro, NC",
        "phone": "",
        "website": "https://www.wakehealth.edu/locations/urgent-care/urgent-care-wilkes",
        "description": "Urgent care services part of the Atrium Health network",
        "status": "Active",
        "tags": ["urgent care", "healthcare"]
    },
    
    # MENTAL HEALTH RESOURCES
    {
        "name": "Daymark Recovery Services - Wilkes County",
        "type": "Healthcare",
        "address": "118 Peace Street, North Wilkesboro, NC 28659",
        "phone": "336-667-7191",
        "email": "",
        "website": "http://www.daymarkrecovery.org/locations/wilkes-county-fbc",
        "description": "Mental health and substance abuse treatment services, including crisis intervention. Open 24/7.",
        "status": "Active",
        "tags": ["mental health", "substance abuse", "crisis services", "24/7"]
    },
    {
        "name": "Daymark Recovery Services Crisis Line",
        "type": "Healthcare",
        "address": "",
        "phone": "336-838-9936",
        "website": "",
        "description": "24-hour crisis mental health hotline for Wilkes County residents",
        "status": "Active",
        "tags": ["mental health", "crisis", "hotline", "24/7"]
    },
    {
        "name": "Monarch - Wilkes County",
        "type": "Healthcare",
        "address": "Wilkes County",
        "phone": "",
        "website": "https://monarchnc.org/county/wilkes/",
        "description": "Outpatient therapy and mental health services for recovery from mental illness",
        "status": "Active",
        "tags": ["mental health", "therapy", "behavioral health"]
    },
    {
        "name": "Jodi Province Counseling Services",
        "type": "Healthcare",
        "address": "Wilkes County",
        "phone": "",
        "website": "https://www.jodiprovincecs.com/",
        "description": "Counseling services for children, adolescents, adults, and families",
        "status": "Active",
        "tags": ["mental health", "counseling", "therapy"]
    },
    {
        "name": "North Wilkesboro Comprehensive Treatment Center",
        "type": "Healthcare",
        "address": "200 Northview Plaza, North Wilkesboro, NC 28659",
        "phone": "866-387-0469",
        "website": "https://www.ctcprograms.com/location/north-wilkesboro-comprehensive-treatment-center/",
        "description": "Outpatient treatment for adults struggling with opioid use disorder",
        "status": "Active",
        "tags": ["substance abuse", "opioid treatment", "recovery"]
    },
    {
        "name": "Stepping Stone of Wilkes",
        "type": "Healthcare",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://pinnacletreatment.com/location/north-carolina/wilkesboro/stepping-stone-of-wilkes/",
        "description": "Suboxone-based treatment and support for opioid recovery",
        "status": "Active",
        "tags": ["substance abuse", "opioid treatment", "recovery"]
    },
    
    # HOUSING & HOMELESS SERVICES
    {
        "name": "Catherine H. Barber Memorial Shelter",
        "type": "Housing",
        "address": "106 Elkin Highway, North Wilkesboro, NC 28659",
        "phone": "336-838-7120",
        "website": "https://wilkeshomelessshelter.org",
        "description": "Emergency homeless shelter providing temporary overnight shelter and one hot meal daily for individuals and families experiencing homelessness",
        "status": "Active",
        "tags": ["homeless shelter", "emergency housing", "food"]
    },
    {
        "name": "Wilkes Housing and Outreach Center (Hospitality House)",
        "type": "Housing",
        "address": "1904 West Park Drive, North Wilkesboro, NC",
        "phone": "",
        "website": "https://highcountrywdb.com/2023/02/wilkes-housing-and-outreach-center/",
        "description": "Housing and outreach services provided by Hospitality House",
        "status": "Active",
        "tags": ["housing assistance", "homeless services"]
    },
    {
        "name": "Hospitality House - Edgecliff Permanent Supportive Housing",
        "type": "Housing",
        "address": "225 Birch St, North Wilkesboro, NC",
        "phone": "",
        "website": "https://www.hosphouse.org/housing",
        "description": "5 apartments for homeless domestic violence survivors with disabling conditions",
        "status": "Active",
        "tags": ["housing", "domestic violence", "supportive housing"]
    },
    {
        "name": "Wilkes Housing Authority",
        "type": "Housing",
        "address": "",
        "phone": "336-667-8979",
        "website": "",
        "description": "Manages public housing units and provides assisted rental housing",
        "status": "Active",
        "tags": ["public housing", "rental assistance", "low income"]
    },
    
    # FOOD ASSISTANCE
    {
        "name": "Samaritan Kitchen of Wilkes",
        "type": "Food",
        "address": "4187 US-421, Wilkesboro, NC",
        "phone": "336-838-5331",
        "website": "https://skwilkes.org",
        "description": "Non-profit organization dedicated to eliminating hunger in the community. Provides evening meals and food pantry services.",
        "status": "Active",
        "tags": ["food pantry", "meals", "hunger relief"]
    },
    {
        "name": "BROC - Meals on Wheels Wilkes County",
        "type": "Food",
        "address": "710 Veterans Dr, North Wilkesboro, NC",
        "phone": "336-667-7174",
        "website": "",
        "description": "Home delivered meals for seniors and homebound individuals",
        "status": "Active",
        "tags": ["meals on wheels", "senior services", "food delivery"]
    },
    {
        "name": "Second Harvest Food Bank of Northwest NC",
        "type": "Food",
        "address": "",
        "phone": "",
        "website": "https://www.secondharvestnwnc.org",
        "description": "Regional food bank serving northwest North Carolina including Wilkes County",
        "status": "Active",
        "tags": ["food bank", "hunger relief"]
    },
    {
        "name": "Wilkes Community College Food Pantry",
        "type": "Food",
        "address": "Wilkes Community College",
        "phone": "",
        "website": "https://www.wilkescc.edu/pantry/",
        "description": "Free food pantry for WCC students offering grab-and-go snack and meal items",
        "status": "Active",
        "tags": ["food pantry", "student services"]
    },
    
    # LEGAL AID
    {
        "name": "Legal Aid of North Carolina",
        "type": "Legal",
        "address": "",
        "phone": "",
        "website": "https://legalaidnc.org",
        "description": "Statewide nonprofit law firm providing free legal services in civil matters to low-income people",
        "status": "Active",
        "tags": ["legal aid", "free legal services", "civil law"]
    },
    {
        "name": "Legal Aid of North Carolina - Winston-Salem Office",
        "type": "Legal",
        "address": "",
        "phone": "",
        "website": "https://www.lawhelpnc.org/organization/legal-aid-of-north-carolina-winston-salem-off",
        "description": "Regional office providing free legal assistance to low-income people in civil cases",
        "status": "Active",
        "tags": ["legal aid", "free legal services"]
    },
    {
        "name": "Pisgah Legal Services",
        "type": "Legal",
        "address": "",
        "phone": "",
        "website": "https://www.pisgahlegal.org",
        "description": "Free attorney services and legal assistance in non-criminal matters for those who cannot afford a private lawyer",
        "status": "Active",
        "tags": ["legal aid", "free legal services"]
    },
    {
        "name": "NC Pro Bono Resource Center",
        "type": "Legal",
        "address": "",
        "phone": "",
        "website": "https://ncprobono.org",
        "description": "Helps North Carolina attorneys find pro bono legal service volunteer opportunities",
        "status": "Active",
        "tags": ["legal aid", "pro bono"]
    },
    
    # SENIOR SERVICES
    {
        "name": "Wilkes Senior Resources / Wilkes Senior Center",
        "type": "Senior Services",
        "address": "228 Fairplains School Road, North Wilkesboro, NC",
        "phone": "336-651-7811",
        "website": "http://www.wilkesseniorresources.com",
        "description": "Provides services, education, and information promoting quality of life and active aging for seniors 55+. Free membership.",
        "status": "Active",
        "tags": ["senior center", "aging services", "senior activities"]
    },
    {
        "name": "Wilkes County Adult Services",
        "type": "Senior Services",
        "address": "Wilkes County",
        "phone": "",
        "website": "https://www.wilkescounty.net/284/Adult-Services",
        "description": "Assists adults and families with decision making and adjustment for out-of-home placements",
        "status": "Active",
        "tags": ["adult services", "senior services"]
    },
    
    # VETERAN SERVICES
    {
        "name": "NC Department of Military & Veterans Affairs",
        "type": "Veteran Services",
        "address": "",
        "phone": "844-624-8387",
        "website": "https://www.milvets.nc.gov",
        "description": "State agency providing services and benefits information for North Carolina veterans",
        "status": "Active",
        "tags": ["veterans", "VA benefits", "military"]
    },
    {
        "name": "Iredell County Veterans Service Office",
        "type": "Veteran Services",
        "address": "200 S. Center Street, Statesville, NC 28677",
        "phone": "",
        "website": "https://www.milvets.nc.gov/services-county/open",
        "description": "County veterans service office providing benefits assistance",
        "status": "Active",
        "tags": ["veterans", "VA benefits"]
    },
    
    # DISABILITY SERVICES
    {
        "name": "Wilkes Vocational Services",
        "type": "Disability Services",
        "address": "North Wilkesboro, NC",
        "phone": "",
        "website": "https://wilkesvs.org",
        "description": "Nonprofit offering employment and community services for adults with disabilities",
        "status": "Active",
        "tags": ["vocational rehabilitation", "disability services", "employment"]
    },
    {
        "name": "NC Division of Vocational Rehabilitation Services - Wilkes",
        "type": "Disability Services",
        "address": "318 Wilkesboro Ave, North Wilkesboro, NC 28659",
        "phone": "336-667-1205",
        "email": "",
        "website": "",
        "description": "Promotes employment and independence for people with disabilities through counseling, training, education, and job placement",
        "status": "Active",
        "tags": ["vocational rehabilitation", "disability services", "employment"]
    },
    {
        "name": "NC DHHS Employment and Independence for People with Disabilities",
        "type": "Disability Services",
        "address": "",
        "phone": "",
        "website": "https://www.ncdhhs.gov/eipd",
        "description": "Helps people with disabilities achieve goals for competitive employment and independent living",
        "status": "Active",
        "tags": ["disability services", "employment", "independent living"]
    },
    
    # TRANSPORTATION
    {
        "name": "Wilkes Transportation Authority (WTA)",
        "type": "Transportation",
        "address": "1010 Spring Street, Wilkesboro, NC 28697",
        "phone": "336-838-1272",
        "website": "http://wta1.org",
        "description": "Public transportation authority providing the Wilkes Express Shuttle (WE Shuttle) Monday, Wednesday, Friday with 25 stops in Wilkesboro and North Wilkesboro. Fares $2-$24.",
        "status": "Active",
        "tags": ["public transit", "shuttle", "transportation"]
    },
    
    # CHILD & FAMILY SERVICES
    {
        "name": "Wilkes County Child Protective Services",
        "type": "Child & Family Services",
        "address": "304 College St., Wilkesboro, NC 28697",
        "phone": "336-651-7400",
        "website": "https://www.ncdhhs.gov/divisions/social-services/child-welfare-services/child-protective-services",
        "description": "Protects children from abuse and neglect, ensures safe and nurturing families",
        "status": "Active",
        "tags": ["child protective services", "child welfare", "family services"]
    },
    {
        "name": "Wilkes County Family Services",
        "type": "Child & Family Services",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://www.wilkescounty.net/295/Family-Services",
        "description": "Assures children receive adequate parental support through locating absent parents, establishing paternity, and providing medical and financial support",
        "status": "Active",
        "tags": ["family services", "child support", "parenting"]
    },
    {
        "name": "Wilkes County Children's Services",
        "type": "Child & Family Services",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://www.wilkescounty.net/289/Childrens-Services",
        "description": "Provides affordable child care services for employed clients and those in training programs",
        "status": "Active",
        "tags": ["child care", "parenting", "family services"]
    },
    {
        "name": "Our House / Child Abuse Prevention Team (CAPT)",
        "type": "Child & Family Services",
        "address": "203 East Main Street, Wilkesboro, NC 28697",
        "phone": "336-667-5555",
        "website": "https://www.facebook.com/ourhousecapt/",
        "description": "Child abuse prevention and family support services",
        "status": "Active",
        "tags": ["child abuse prevention", "family support"]
    },
    {
        "name": "Safe Spot Wilkes",
        "type": "Child & Family Services",
        "address": "",
        "phone": "336-838-7233",
        "website": "https://www.safespotwilkes.org",
        "description": "Child advocacy center providing services for children who have experienced abuse",
        "status": "Active",
        "tags": ["child advocacy", "child abuse", "family services"]
    },
    
    # DOMESTIC VIOLENCE RESOURCES
    {
        "name": "DANA Services of NC",
        "type": "Domestic Violence",
        "address": "Alleghany County",
        "phone": "",
        "website": "https://www.danaservices.org",
        "description": "Domestic Abuse is Not Acceptable - serves victims of domestic abuse and sexual assault in Alleghany County and surrounding areas",
        "status": "Active",
        "tags": ["domestic violence", "sexual assault", "crisis services"]
    },
    {
        "name": "NC Coalition Against Domestic Violence",
        "type": "Domestic Violence",
        "address": "",
        "phone": "",
        "website": "https://nccadv.org/get-help/",
        "description": "Statewide coalition providing resources and referrals to local domestic violence agencies serving all 100 NC counties",
        "status": "Active",
        "tags": ["domestic violence", "hotline", "shelter"]
    },
    
    # COMMUNITY ORGANIZATIONS
    {
        "name": "United Way of Wilkes County",
        "type": "Community Organization",
        "address": "",
        "phone": "",
        "website": "https://uwwilkes.org",
        "description": "Supports local families, children, and neighbors in need - building a stronger, healthier community",
        "status": "Active",
        "tags": ["nonprofit", "community support", "funding"]
    },
    {
        "name": "Wilkes Community Foundation",
        "type": "Community Organization",
        "address": "",
        "phone": "",
        "website": "https://www.nccommunityfoundation.org/affiliate/wilkes-community-foundation",
        "description": "Growing family of philanthropic funds providing grants for local causes",
        "status": "Active",
        "tags": ["nonprofit", "philanthropy", "grants"]
    },
    {
        "name": "Wilkes Chamber of Commerce",
        "type": "Community Organization",
        "address": "",
        "phone": "",
        "website": "https://business.wilkeschamber.org",
        "description": "Business organization supporting local commerce and economic development",
        "status": "Active",
        "tags": ["chamber of commerce", "business", "economic development"]
    },
    {
        "name": "Wilkes Economic Development Corporation",
        "type": "Community Organization",
        "address": "",
        "phone": "",
        "website": "https://wilkesedc.com",
        "description": "Promotes economic growth and development in Wilkes County",
        "status": "Active",
        "tags": ["economic development", "business", "jobs"]
    },
    
    # NEWS SOURCES
    {
        "name": "Wilkes Journal-Patriot",
        "type": "News",
        "address": "316 Wilkesboro Ave., North Wilkesboro, NC",
        "phone": "",
        "website": "https://www.journalpatriot.com",
        "description": "Weekly newspaper serving Wilkes County since 1906, published Thursdays",
        "status": "Active",
        "tags": ["newspaper", "local news", "media"]
    },
    {
        "name": "Watauga Democrat",
        "type": "News",
        "address": "",
        "phone": "",
        "website": "https://www.wataugademocrat.com",
        "description": "Local newspaper serving Watauga County and the High Country including Boone",
        "status": "Active",
        "tags": ["newspaper", "local news", "media"]
    },
    
    # EMERGENCY SERVICES
    {
        "name": "Wilkes County Emergency Medical Services (EMS)",
        "type": "Emergency Services",
        "address": "204 Call Street, Wilkesboro, NC 28697",
        "phone": "",
        "website": "https://wilkescounty.net/535/Emergency-Medical-Services---EMS",
        "description": "Responds to over 12,000 calls per year providing 911 and non-emergency medical care",
        "status": "Active",
        "tags": ["EMS", "emergency", "medical", "911"]
    },
    {
        "name": "Wilkes County Emergency Management",
        "type": "Emergency Services",
        "address": "",
        "phone": "",
        "website": "https://www.iredelleoc.com",
        "description": "Coordinates emergency preparedness, response, and recovery for the county",
        "status": "Active",
        "tags": ["emergency management", "disaster preparedness"]
    },
    {
        "name": "Wilkes County Sheriff's Office",
        "type": "Emergency Services",
        "address": "110 North Street, Wilkesboro, NC 28697",
        "phone": "336-903-7600",
        "website": "https://wilkescounty.net/151/Sheriff",
        "description": "County law enforcement agency",
        "status": "Active",
        "tags": ["law enforcement", "sheriff", "public safety"]
    },
    
    # UTILITIES
    {
        "name": "Town of Wilkesboro Utilities Department",
        "type": "Utilities",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://wilkesboronc.org/47-utilities-dept",
        "description": "Provides water and sanitary sewer service to over 1,800 metered customers",
        "status": "Active",
        "tags": ["water", "sewer", "utilities"]
    },
    {
        "name": "Town of North Wilkesboro Public Services",
        "type": "Utilities",
        "address": "North Wilkesboro, NC",
        "phone": "",
        "website": "https://www.north-wilkesboro.com",
        "description": "Provides water, sewer, and sanitation services",
        "status": "Active",
        "tags": ["water", "sewer", "sanitation", "utilities"]
    },
    
    # LIBRARIES
    {
        "name": "Wilkes County Public Library",
        "type": "Library",
        "address": "215 10th Street, North Wilkesboro, NC 28659",
        "phone": "336-838-2818",
        "email": "",
        "website": "https://www.arlibrary.org/wilkes",
        "description": "Public library serving Wilkes County as part of the Appalachian Regional Library system (serving Ashe, Wilkes, and Watauga counties)",
        "status": "Active",
        "tags": ["library", "books", "education", "community"]
    },
    
    # EDUCATION
    {
        "name": "Wilkes County Schools",
        "type": "Education",
        "address": "",
        "phone": "",
        "website": "https://www.wilkescountyschools.org",
        "description": "Public school district serving Wilkes County with 22 schools K-12",
        "status": "Active",
        "tags": ["public schools", "K-12", "education"]
    },
    {
        "name": "Wilkes Community College",
        "type": "Education",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://www.wilkescc.edu",
        "description": "Community college offering degree programs, workforce training, and continuing education",
        "status": "Active",
        "tags": ["college", "higher education", "workforce training"]
    },
    
    # EMPLOYMENT & TRAINING
    {
        "name": "NCWorks Career Center - Wilkes County",
        "type": "Employment",
        "address": "North Wilkesboro, NC",
        "phone": "",
        "website": "https://www.ncworks.gov",
        "description": "Career center providing job search assistance, career planning, training, and job placement services",
        "status": "Active",
        "tags": ["employment", "job search", "career services", "training"]
    },
    {
        "name": "NCWorks Career Center - Wilkesboro (Goodwill)",
        "type": "Employment",
        "address": "Wilkesboro, NC",
        "phone": "",
        "website": "https://www.goodwillnwnc.org/locations/ncworks-career-center-wilkesboro/",
        "description": "NCWorks career center hosted by Goodwill providing employment services",
        "status": "Active",
        "tags": ["employment", "job search", "career services"]
    },
]

def add_resources():
    """Add discovered resources to Supabase database."""
    print("=" * 60)
    print("DEEP RESEARCH AGENT - Adding Resources to Supabase")
    print("=" * 60)
    print()
    
    try:
        supabase = get_supabase()
        print("✓ Connected to Supabase")
        print()
        
        # Check if resources table exists
        try:
            result = supabase.table("resources").select("count").limit(1).execute()
            print("✓ Resources table exists")
        except Exception as e:
            print(f"✗ Resources table error: {e}")
            print("  Creating resources table...")
            return
        
        print()
        print(f"Adding {len(RESOURCES)} resources...")
        print()
        
        added_count = 0
        error_count = 0
        
        for resource in RESOURCES:
            try:
                # Add timestamp
                resource["created_at"] = datetime.now(timezone.utc).isoformat()
                
                # Insert into Supabase
                result = supabase.table("resources").insert(resource).execute()
                
                if result.data:
                    print(f"  ✓ Added: {resource['name']}")
                    added_count += 1
                else:
                    print(f"  ✗ Failed: {resource['name']}")
                    error_count += 1
                    
            except Exception as e:
                # Check if it's a duplicate error
                error_str = str(e)
                if "duplicate" in error_str.lower() or "already exists" in error_str.lower() or "23505" in error_str:
                    print(f"  ⚠ Duplicate: {resource['name']}")
                else:
                    print(f"  ✗ Error adding {resource['name']}: {e}")
                error_count += 1
        
        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Total resources: {len(RESOURCES)}")
        print(f"  Successfully added: {added_count}")
        print(f"  Errors/Duplicates: {error_count}")
        print()
        
        # Show breakdown by type
        type_counts = {}
        for r in RESOURCES:
            t = r.get("type", "Unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        
        print("Resources by type:")
        for t, count in sorted(type_counts.items()):
            print(f"  - {t}: {count}")
        print()
        
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_resources()
