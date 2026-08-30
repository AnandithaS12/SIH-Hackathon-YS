import asyncio
from datetime import datetime
from lib.db import db
from models.scheme import Scheme
from models.document import MasterDocument

SCHEMES_DATA = [
    {
        "id": "pm-kisan",
        "title": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "title_hi": "प्रधानमंत्री किसान सम्मान निधि (पीएम-किसान)",
        "short_name": "PM-KISAN",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "sector": "Agriculture",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "PM-KISAN is a flagship Central Sector Scheme offering income support of ₹6,000 per annum to all landholding farmer families across the country in three equal installments of ₹2,000 every 4 months directly into bank accounts via Direct Benefit Transfer (DBT).",
        "benefit_summary": "₹6,000 per year directly in 3 installments of ₹2,000 via Aadhaar-linked DBT",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹6,000 / year",
        "eligibility_criteria": [
            "All landholding farmer families with cultivable land in their names",
            "Valid Aadhaar card linked with active bank account and eKYC completed",
            "Excludes institutional landholders, serving/retired government officials, and income tax payees"
        ],
        "target_beneficiaries": ["Small & Marginal Farmers", "Landholding Farm Families"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Farmer / Agriculture", "Fisherfolk / Dairy Farmer"],
            "requires_land": True,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "For biometric eKYC and identity verification", "how_to_get": "Download via UIDAI portal or visit Aadhaar Seva Kendra"},
            {"name": "Land Ownership Record (Khatauni / RoR / 7-12)", "mandatory": True, "description": "Proof of agricultural cultivable landholding", "how_to_get": "Obtain from State Bhulekh / Revenue portal or Tehsildar"},
            {"name": "Bank Account Passbook (Aadhaar & NPCI linked)", "mandatory": True, "description": "For direct benefit credit into DBT enabled account", "how_to_get": "Visit your bank branch and complete Aadhaar seeding"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Visit Official Portal", "description": "Open https://pmkisan.gov.in and click on 'New Farmer Registration' under Farmers Corner."},
            {"step_number": 2, "title": "Aadhaar & Mobile Authentication", "description": "Enter your 12-digit Aadhaar number, state, and registered mobile OTP."},
            {"step_number": 3, "title": "Enter Land & Bank Details", "description": "Input land survey number, Khasra/Khatauni details, area in hectares, and bank IFSC."},
            {"step_number": 4, "title": "Submit & Complete eKYC", "description": "Submit application and complete mandatory biometric/OTP eKYC to activate installment disbursement."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://pmkisan.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-kisan-samman-nidhi-pm-kisan",
        "helpline": "155261 / 011-24300606 / 1800-115-526",
        "faq": [
            {"question": "How often is the ₹2,000 installment paid?", "answer": "Every four months (Period 1: April-July, Period 2: August-November, Period 3: December-March)."},
            {"question": "Is eKYC mandatory for PM-KISAN?", "answer": "Yes, OTP-based or biometric eKYC on pmkisan.gov.in or CSC centers is mandatory for releasing funds."}
        ],
        "tags": ["farmer", "agriculture", "dbt", "cash", "central"],
        "featured": True
    },
    {
        "id": "ayushman-bharat-pmjay",
        "title": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
        "title_hi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना (पीएम-जय)",
        "short_name": "PM-JAY Ayushman Card",
        "ministry": "Ministry of Health and Family Welfare",
        "sector": "Healthcare",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "World's largest government-funded healthcare assurance scheme offering ₹5,00,000 per family per year for secondary and tertiary care hospitalization across 28,000+ empaneled public and private hospitals across India. Includes all senior citizens aged 70+ irrespective of income.",
        "benefit_summary": "₹5,00,000 per family per year cashless and paperless treatment at empaneled hospitals",
        "benefit_type": "Health Coverage",
        "max_financial_benefit": "₹5,00,000 / family / year",
        "eligibility_criteria": [
            "Households identified under SECC 2011 rural and urban deprivation criteria",
            "Holders of Antyodaya / BPL / Priority Ration Cards",
            "All senior citizens aged 70 years and above (Universal Coverage under Ayushman Vay Vandana Card)",
            "Active unorganized workers registered on e-Shram"
        ],
        "target_beneficiaries": ["Low Income Families", "Senior Citizens (70+)", "BPL Cardholders", "Unorganized Workers"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 100,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "max_annual_income": 300000,
            "requires_bpl": False,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Primary identity verification for golden Ayushman card generation", "how_to_get": "UIDAI portal / nearest CSC"},
            {"name": "Ration Card / Family ID", "mandatory": True, "description": "Proof of family members listed under eligibility pool", "how_to_get": "State Food & Civil Supplies portal"},
            {"name": "Mobile Number", "mandatory": True, "description": "For OTP verification during eKYC and hospital admission", "how_to_get": "Linked mobile"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Check Eligibility Online", "description": "Visit https://beneficiary.nha.gov.in or download the Ayushman App."},
            {"step_number": 2, "title": "Search by Mobile / Ration Card", "description": "Enter your mobile number and search your family via Ration Card or Aadhaar number."},
            {"step_number": 3, "title": "Perform eKYC", "description": "Authenticate via Aadhaar OTP, Face RD app, or Fingerprint at nearest CSC or empaneled hospital kiosk."},
            {"step_number": 4, "title": "Download Ayushman Card (Golden Card)", "description": "Instantly download your PVC Ayushman Card and present at any empaneled hospital for 100% cashless treatment."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://beneficiary.nha.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/ayushman-bharat-national-health-protection-mission",
        "helpline": "14555 / 1800-111-565",
        "faq": [
            {"question": "Does Ayushman Bharat cover pre-existing diseases?", "answer": "Yes, all pre-existing conditions are covered from day one of card activation."},
            {"question": "Are senior citizens aged 70+ covered regardless of income?", "answer": "Yes, under the 2024 expansion, every citizen aged 70+ gets a dedicated ₹5 Lakhs Ayushman Vay Vandana card."}
        ],
        "tags": ["healthcare", "health insurance", "hospital", "cashless", "central"],
        "featured": True
    },
    {
        "id": "pm-awas-gramin",
        "title": "Pradhan Mantri Awas Yojana - Gramin (PMAY-G)",
        "title_hi": "प्रधानमंत्री आवास योजना - ग्रामीण (पीएमएवाई-जी)",
        "short_name": "PMAY-G Housing",
        "ministry": "Ministry of Rural Development",
        "sector": "Housing & Sanitation",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Provides financial assistance to homeless and households living in kutcha or dilapidated houses in rural India to construct a 25 sq.m disaster-resilient pucca house with basic amenities including piped water, electricity, and LPG connection.",
        "benefit_summary": "₹1,20,000 (Plain areas) / ₹1,30,000 (Hilly/NE/Difficult areas) grant + ₹12,000 toilet assistance + 90 days MGNREGA wages",
        "benefit_type": "Housing Grant",
        "max_financial_benefit": "₹1,30,000 + ₹12,000 Toilet + MGNREGA Wages",
        "eligibility_criteria": [
            "Rural houseless households or families living in 0, 1, or 2 room kutcha wall/kutcha roof houses",
            "Priority to SC, ST, Minorities, Widows, PwD, and families without able-bodied adult members",
            "Family must not own a pucca house anywhere in India"
        ],
        "target_beneficiaries": ["Rural Homeless", "Kutcha House Residents", "BPL Families", "SC/ST"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "max_annual_income": 200000,
            "area_type": "rural"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity of all adult family members", "how_to_get": "UIDAI"},
            {"name": "Bank Account Passbook", "mandatory": True, "description": "Direct transfer of construction milestone installments", "how_to_get": "Bank branch"},
            {"name": "MGNREGA Job Card", "mandatory": True, "description": "For claiming 90/95 days of unskilled construction wages", "how_to_get": "Gram Panchayat / Block Development Office"},
            {"name": "Land / House Site Ownership Document", "mandatory": True, "description": "Proof of residential plot in village", "how_to_get": "Panchayat Secretary / Revenue Patwari"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Gram Sabha Beneficiary Listing", "description": "Names are verified through Awaas+ surveys and approved in the Gram Sabha meeting."},
            {"step_number": 2, "title": "Geo-Tagging Stage 1 (Existing Site)", "description": "Panchayat official inspects and geo-tags the existing kutcha house on the AwaasSoft app."},
            {"step_number": 3, "title": "Sanction Order & First Installment", "description": "Direct credit of ₹40,000 into bank account to lay the plinth level foundation."},
            {"step_number": 4, "title": "Subsequent Geo-tagging & Completion", "description": "Subsequent installments released at lintel and roof completion stages."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://pmayg.nic.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-awaas-yojana-gramin",
        "helpline": "1800-11-6446 / 011-23063285",
        "faq": [
            {"question": "How are the funds disbursed?", "answer": "Directly into the beneficiary's Aadhaar-linked bank account in 3 to 4 stages linked to geo-tagged physical progress."}
        ],
        "tags": ["housing", "rural", "pucca house", "grant", "central"],
        "featured": True
    },
    {
        "id": "pm-vishwakarma",
        "title": "PM Vishwakarma Kaushal Samman Yojana",
        "title_hi": "पीएम विश्वकर्मा कौशल सम्मान योजना",
        "short_name": "PM Vishwakarma",
        "ministry": "Ministry of Micro, Small and Medium Enterprises",
        "sector": "Employment & MSME",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Holistic scheme to empower traditional artisans and craftspeople across 18 trades (Carpenters, Blacksmiths, Goldsmiths, Potters, Sculptors, Cobblers, Masons, Weavers, Tailors, etc.) providing PM Vishwakarma Certificate & ID Card, basic/advanced skill training with ₹500/day stipend, ₹15,000 toolkit digital voucher, and collateral-free enterprise credit up to ₹3,00,000 at a concessional 5% interest rate.",
        "benefit_summary": "₹3,00,000 Collateral-free loan @ 5% + ₹15,000 Tool voucher + ₹500/day stipend + Official ID Card",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "₹3,00,000 Loan @ 5% + ₹15,000 Grant",
        "eligibility_criteria": [
            "Artisans and craftspeople working with hands and tools in one of 18 notified traditional family trades",
            "Minimum age of 18 years on the date of registration",
            "Engaged in the trade on the date of application and not availed similar credit (PMEGP/Mudra/PM SVANidhi) in last 5 years",
            "Registration limited to one member per family"
        ],
        "target_beneficiaries": ["Artisans", "Craftsmen", "Traditional Trade Workers", "Carpenters", "Goldsmiths", "Masons", "Tailors"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 75,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Artisan / Craftsman (Vishwakarma)", "Self-Employed / Micro Business", "Daily Wage Laborer / Construction Worker"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Primary biometric verification", "how_to_get": "UIDAI"},
            {"name": "Bank Account Passbook", "mandatory": True, "description": "For receiving ₹15,000 toolkit voucher and loan disbursement", "how_to_get": "Bank branch"},
            {"name": "Skill / Trade Self-Declaration", "mandatory": True, "description": "Declaration of active work in one of the 18 eligible trades", "how_to_get": "Filled at CSC center"},
            {"name": "Ration Card", "mandatory": False, "description": "For family verification", "how_to_get": "Food department"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Visit Nearest CSC", "description": "Visit Common Service Center (CSC) with Aadhaar and mobile for biometric registration."},
            {"step_number": 2, "title": "Gram Panchayat / ULB Verification", "description": "Stage 1 verification done by Panchayat Secretary or Executive Officer."},
            {"step_number": 3, "title": "District Committee Approval", "description": "District Implementation Committee screens and approves the artisan profile."},
            {"step_number": 4, "title": "Skill Training & Loan Disbursement", "description": "Undergo 5-7 days basic skill training (with ₹500/day stipend), receive ₹15,000 e-voucher for tools, and apply for Tranche 1 (₹1 Lakh) loan."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://pmvishwakarma.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pm-vishwakarma-scheme",
        "helpline": "1800-267-7777 / 011-23061500",
        "faq": [
            {"question": "What are the loan tranches?", "answer": "Tranche 1: ₹1,00,000 (18 months tenure) @ 5% interest; Tranche 2: ₹2,00,000 (30 months tenure) after timely repayment of Tranche 1."}
        ],
        "tags": ["artisan", "vishwakarma", "loan", "toolkit", "msme", "central"],
        "featured": True
    },
    {
        "id": "pm-svanidhi",
        "title": "PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)",
        "title_hi": "पीएम स्वनिधि (प्रधानमंत्री स्ट्रीट वेंडर्स आत्मनिर्भर निधि)",
        "short_name": "PM SVANidhi",
        "ministry": "Ministry of Housing and Urban Affairs",
        "sector": "Employment & MSME",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Special micro-credit facility empowering urban, peri-urban and rural street vendors to restart their livelihoods with collateral-free working capital loans of ₹10,000, ₹20,000, and up to ₹50,000 with 7% interest subsidy and cashback of up to ₹1,200 per year on digital transactions.",
        "benefit_summary": "Collateral-free working capital loans of ₹10k, ₹20k, ₹50k with 7% interest subsidy & ₹1,200 digital cashback",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "Up to ₹50,000 Loan @ 7% Subsidy",
        "eligibility_criteria": [
            "Street vendors / hawkers operating in urban areas on or before March 24, 2020 or holding a Vending Certificate / LOR",
            "Vendors from surrounding peri-urban and rural areas vending in geographical limits of Urban Local Bodies (ULBs)",
            "Possession of Letter of Recommendation (LoR) issued by ULB / Town Vending Committee"
        ],
        "target_beneficiaries": ["Street Vendors", "Vegetable/Fruit Hawkers", "Food Stalls", "Artisans in Urban Areas"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 70,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Street Vendor / Hawkers", "Self-Employed / Micro Business"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity and mobile authentication", "how_to_get": "UIDAI"},
            {"name": "Vending Certificate / Letter of Recommendation (LoR)", "mandatory": True, "description": "Issued by Municipality / Town Vending Committee", "how_to_get": "Apply online at pmsvanidhi.mohua.gov.in or visit Municipality office"},
            {"name": "Bank Passbook", "mandatory": True, "description": "For direct loan credit and digital QR code mapping", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Check LoR / Vending Status", "description": "Search your name in the Town Vending list or apply for Letter of Recommendation on https://pmsvanidhi.mohua.gov.in."},
            {"step_number": 2, "title": "Apply for 1st Tranche Loan (₹10,000)", "description": "Select lending bank (Public bank, Regional Rural Bank, or MFI) and submit Aadhaar OTP."},
            {"step_number": 3, "title": "Loan Approval & Sanction", "description": "Lending partner processes and disburses loan within 7-14 days without any physical collateral."},
            {"step_number": 4, "title": "Digital Onboarding & Upgrades", "description": "Receive UPI QR code, earn ₹100/month cashback, and unlock ₹20k & ₹50k tranches upon timely repayment."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://pmsvanidhi.mohua.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pm-street-vendors-atmanirbhar-nidhi-pm-svanidhi",
        "helpline": "1800-11-1979 / 011-23062329",
        "faq": [
            {"question": "What is the interest subsidy rate?", "answer": "7% interest subsidy is credited directly into the borrower's bank account on a quarterly basis."}
        ],
        "tags": ["vendor", "working capital", "loan", "urban", "subsidy", "central"],
        "featured": True
    },
    {
        "id": "pm-mudra-yojana",
        "title": "Pradhan Mantri Mudra Yojana (PMMY)",
        "title_hi": "प्रधानमंत्री मुद्रा योजना (पीएमएमवाई)",
        "short_name": "PM Mudra Loan",
        "ministry": "Ministry of Finance",
        "sector": "Employment & MSME",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Enables micro and small enterprises engaged in manufacturing, trading, and services to access collateral-free institutional credit up to ₹20,00,000 across four categories: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 Lakhs), Tarun (₹5 Lakhs to ₹10 Lakhs), and Tarun Plus (up to ₹20 Lakhs).",
        "benefit_summary": "Collateral-free business loans up to ₹20 Lakhs with Mudra Debit Card for working capital",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "Up to ₹20,00,000 Collateral-Free Loan",
        "eligibility_criteria": [
            "Non-farm micro or small business enterprises in manufacturing, processing, trade or services sector",
            "Any Indian citizen who has a business plan for non-farming income generating activity",
            "Applicant must not be a defaulter to any bank or financial institution"
        ],
        "target_beneficiaries": ["Micro Entrepreneurs", "Shopkeepers", "Small Manufacturers", "Food Processors", "Women Entrepreneurs"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 65,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Self-Employed / Micro Business", "Artisan / Craftsman (Vishwakarma)", "Street Vendor / Hawkers"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card & PAN Card", "mandatory": True, "description": "Identity and KYC verification", "how_to_get": "UIDAI / Income Tax portal"},
            {"name": "Proof of Business Establishment (Udyam / Shop Act)", "mandatory": True, "description": "Registration of enterprise / trade license", "how_to_get": "Free registration on udyamregistration.gov.in"},
            {"name": "Bank Statement (Last 6 Months)", "mandatory": True, "description": "Proof of financial operations and turnover", "how_to_get": "Bank branch / Netbanking"},
            {"name": "Project Proposal / Quotation for Machinery", "mandatory": False, "description": "Required for Kishore and Tarun category loans", "how_to_get": "Prepared by applicant or CA"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on JanSamarth Portal", "description": "Visit https://www.jansamarth.in/business-activity-loan-schemes and select PM Mudra Yojana."},
            {"step_number": 2, "title": "Check Eligibility & Select Category", "description": "Choose between Shishu (up to ₹50k), Kishore (up to ₹5L), or Tarun (up to ₹20L)."},
            {"step_number": 3, "title": "Upload KYC & Business Details", "description": "Upload PAN, Udyam Registration number, and bank account statement."},
            {"step_number": 4, "title": "Get Digital In-Principle Approval", "description": "Compare partner bank offers and receive digital sanction with Mudra Card."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.mudra.org.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-mudra-yojana",
        "helpline": "1800-180-1111 / 1800-11-0001",
        "faq": [
            {"question": "Is collateral or security required for Mudra loan?", "answer": "No, loans under PMMY are 100% collateral-free and backed by Credit Guarantee for Micro Units (CGFMU)."}
        ],
        "tags": ["mudra", "business loan", "msme", "credit", "central"],
        "featured": True
    },
    {
        "id": "pm-matru-vandana",
        "title": "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
        "title_hi": "प्रधानमंत्री मातृ वंदना योजना (पीएमएमवीवाई)",
        "short_name": "PMMVY Maternity Benefit",
        "ministry": "Ministry of Women and Child Development",
        "sector": "Women & Child",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Direct maternity cash incentive of ₹5,000 (in 2 installments) for the first living child and ₹6,000 (in a single installment) for a second child if it is a girl, compensating wage loss before and after delivery and encouraging institutional delivery and child immunization.",
        "benefit_summary": "₹5,000 for 1st child (2 installments) + ₹6,000 for 2nd girl child via direct cash transfer",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹5,000 - ₹6,000 DBT",
        "eligibility_criteria": [
            "Pregnant Women and Lactating Mothers (PW&LM) who have registered their pregnancy at Anganwadi / Health Center",
            "Excludes women in regular central/state government employment or public sector undertakings",
            "Must possess Mother and Child Protection (MCP) Card and Aadhaar"
        ],
        "target_beneficiaries": ["Pregnant Women", "Lactating Mothers", "Low-Income Families"],
        "eligibility_rules": {
            "min_age": 19,
            "max_age": 45,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["All"],
            "requires_pregnant_lactating": True,
            "max_annual_income": 800000,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Mother and Child Protection (MCP) Card", "mandatory": True, "description": "Proof of ANC checkup and child immunization", "how_to_get": "Issued by Anganwadi Worker / ANM / Govt Hospital"},
            {"name": "Aadhaar Card of Mother & Husband", "mandatory": True, "description": "Identity and demographic proof", "how_to_get": "UIDAI"},
            {"name": "Bank / Post Office Passbook of Mother", "mandatory": True, "description": "Individual account linked with Aadhaar", "how_to_get": "Bank branch / Post office"},
            {"name": "Child Birth Certificate", "mandatory": True, "description": "Required for 2nd installment / girl child incentive", "how_to_get": "Municipal Corporation / Panchayat"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register at Anganwadi / PMMVY Portal", "description": "Visit local Anganwadi Centre (AWC) or register directly on https://pmmvy.wcd.gov.in within 270 days of LMP date."},
            {"step_number": 2, "title": "Submit 1st Installment Claim (₹3,000)", "description": "Claim after early registration of pregnancy and at least one Ante-Natal Check-up (ANC)."},
            {"step_number": 3, "title": "Submit 2nd Installment Claim (₹2,000 / ₹6,000)", "description": "Claim after child birth registration and completion of first cycle of vaccination (BCG, OPV, DPT, Hepatitis-B)."}
        ],
        "application_mode": "Hybrid",
        "official_portal_url": "https://pmmvy.wcd.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-matru-vandana-yojana",
        "helpline": "011-23382393 / 1098 / 14408",
        "faq": [
            {"question": "Can I apply for the second child?", "answer": "Yes, if the second child is a girl, you receive a special one-time incentive of ₹6,000 directly to curb female feticide."}
        ],
        "tags": ["women", "maternity", "cash transfer", "nutrition", "central"],
        "featured": True
    },
    {
        "id": "sukanya-samriddhi-yojana",
        "title": "Sukanya Samriddhi Yojana (SSY)",
        "title_hi": "सुकन्या समृद्धि योजना (एसएसवाई)",
        "short_name": "Sukanya Samriddhi",
        "ministry": "Ministry of Finance",
        "sector": "Women & Child",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Flagship small-deposit savings scheme under Beti Bachao Beti Padhao campaign offering government-backed highest interest rate (currently 8.2% p.a., compounded annually) and triple tax exemption (EEE under 80C) for a girl child from birth up to 10 years of age.",
        "benefit_summary": "8.2% Guaranteed interest rate with complete tax-free maturity amount for girl child education & marriage",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "8.2% Annual Interest + EEE Tax Benefit",
        "eligibility_criteria": [
            "Account can be opened by natural or legal guardians in the name of a girl child from birth until she attains 10 years of age",
            "Maximum 2 girl child accounts per family (or 3 in case of firstborn triplets/twins)",
            "Minimum deposit of ₹250 and maximum ₹1,50,000 in a financial year"
        ],
        "target_beneficiaries": ["Girl Children under 10 years", "Parents/Guardians"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 60,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "requires_girl_child": True,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Girl Child Birth Certificate", "mandatory": True, "description": "Proof of age and parentage", "how_to_get": "Registrar of Births & Deaths / Municipality"},
            {"name": "Aadhaar & PAN of Parent/Guardian", "mandatory": True, "description": "KYC proof of guardian", "how_to_get": "UIDAI / Income Tax"},
            {"name": "Passport Sized Photographs", "mandatory": True, "description": "Photos of child and guardian", "how_to_get": "Local studio / digital photo"},
            {"name": "Address Proof", "mandatory": True, "description": "Electricity bill / Ration card / Aadhaar", "how_to_get": "Utility bill"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Visit Post Office or Authorized Bank", "description": "Go to any India Post branch or authorized commercial bank (SBI, PNB, BoB, ICICI, etc.)."},
            {"step_number": 2, "title": "Fill SSY Account Form-1", "description": "Provide child's name, DOB, guardian details, and initial deposit amount (min ₹250)."},
            {"step_number": 3, "title": "Submit KYC & Birth Certificate", "description": "Attach attested copies of birth certificate and guardian Aadhaar/PAN."},
            {"step_number": 4, "title": "Receive Passbook", "description": "Collect SSY passbook with unique account number for annual deposits and online tracking."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://www.indiapost.gov.in/Financial/Pages/Content/Sukanya-Samriddhi-Account.aspx",
        "india_gov_url": "https://www.india.gov.in/sukanya-samriddhi-yojana",
        "helpline": "1800-266-6868",
        "faq": [
            {"question": "When does the account mature?", "answer": "The account matures 21 years from the date of opening or upon the girl's marriage after attaining 18 years of age. Partial withdrawal (50%) is allowed for higher education after age 18."}
        ],
        "tags": ["girl child", "savings", "tax free", "education", "central"],
        "featured": True
    },
    {
        "id": "lakhpati-didi",
        "title": "Lakhpati Didi Scheme (Mission Shakti)",
        "title_hi": "लखपति दीदी योजना (मिशन शक्ति)",
        "short_name": "Lakhpati Didi",
        "ministry": "Ministry of Rural Development",
        "sector": "Women & Child",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "National initiative to empower 3 Crore rural women Self-Help Group (SHG) members to earn a sustainable annual household income of at least ₹1,00,000 (₹1 Lakh) through specialized technical training (drone pilot / Drone Didi, solar technician, organic farming, LED bulb assembly) and interest-subvention bank loans up to ₹5 Lakhs.",
        "benefit_summary": "₹1 Lakh+ Annual income capability through free micro-enterprise training, drone piloting, and loans up to ₹5 Lakhs",
        "benefit_type": "Free Training & Certification",
        "max_financial_benefit": "Skill Training + Up to ₹5 Lakhs SHG Credit @ Low Interest",
        "eligibility_criteria": [
            "Rural women active in a Deendayal Antyodaya Yojana - National Rural Livelihoods Mission (DAY-NRLM) Self Help Group",
            "Age between 18 and 55 years",
            "Committed to taking up micro-enterprises or agricultural value-addition activities"
        ],
        "target_beneficiaries": ["Rural Women", "SHG Members", "Women Entrepreneurs"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 55,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["Homemaker", "Farmer / Agriculture", "Self-Employed / Micro Business", "Artisan / Craftsman (Vishwakarma)"],
            "area_type": "rural"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Individual identity proof", "how_to_get": "UIDAI"},
            {"name": "SHG Member Passbook / ID", "mandatory": True, "description": "Proof of active membership in village SHG", "how_to_get": "SHG President / Community Resource Person (CRP)"},
            {"name": "Bank Account Details", "mandatory": True, "description": "Individual & SHG group bank account", "how_to_get": "Bank branch"},
            {"name": "Ration Card", "mandatory": False, "description": "Proof of family economic background", "how_to_get": "Food department"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Enroll through Village SHG", "description": "Contact your Village Organization (VO) / Cluster Level Federation (CLF) under DAY-NRLM."},
            {"step_number": 2, "title": "Select Enterprise / Skill Track", "description": "Choose trade such as Namo Drone Didi, food processing, animal husbandry, tailoring, or solar repair."},
            {"step_number": 3, "title": "Undergo Specialized Training", "description": "Complete free training at Rural Self Employment Training Institutes (RSETI) or Krishi Vigyan Kendra."},
            {"step_number": 4, "title": "Avail Community Investment Fund (CIF)", "description": "Receive business start-up capital and bank linkage loans to scale your micro-venture."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://nrlm.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/lakhpati-didi-initiative",
        "helpline": "011-23383553 / 1800-180-6127",
        "faq": [
            {"question": "What is the Drone Didi component?", "answer": "15,000 selected women SHGs receive free agricultural drones, 15-day certified pilot training, and ₹15,000 monthly rental income opportunity for spraying fertilizers/pesticides."}
        ],
        "tags": ["women", "shg", "drone didi", "rural enterprise", "central"],
        "featured": True
    },
    {
        "id": "atal-pension-yojana",
        "title": "Atal Pension Yojana (APY)",
        "title_hi": "अटल पेंशन योजना (एपीवाई)",
        "short_name": "Atal Pension",
        "ministry": "Ministry of Finance",
        "sector": "Financial Inclusion & Pension",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Government-backed guaranteed pension scheme for unorganized sector workers, providing a fixed monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000, or ₹5,000 per month from age 60 until demise, followed by full pension to spouse and return of accumulated pension wealth to nominee.",
        "benefit_summary": "Guaranteed lifetime monthly pension of ₹1,000 to ₹5,000 from age 60 + full spouse pension & corpus return",
        "benefit_type": "Pension",
        "max_financial_benefit": "₹5,000 / month lifetime guaranteed pension",
        "eligibility_criteria": [
            "Any Indian citizen aged between 18 and 40 years",
            "Must have a savings bank account linked with Aadhaar",
            "Applicant must not be an income tax payer as of October 1, 2022"
        ],
        "target_beneficiaries": ["Unorganized Workers", "Gig/Daily Wage Workers", "Self-Employed", "Small Businessmen"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 40,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity and KYC verification", "how_to_get": "UIDAI"},
            {"name": "Savings Bank Account Passbook", "mandatory": True, "description": "For auto-debit of monthly/quarterly contribution", "how_to_get": "Bank branch"},
            {"name": "Active Mobile Number", "mandatory": True, "description": "For transaction alerts and PRAN generation", "how_to_get": "Mobile provider"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Visit Your Bank Branch / Netbanking", "description": "Log into your bank's netbanking portal (SBI, PNB, HDFC, etc.) or visit branch."},
            {"step_number": 2, "title": "Fill APY Subscriber Registration Form", "description": "Select monthly pension slab (₹1k to ₹5k) and auto-debit frequency (monthly/quarterly)."},
            {"step_number": 3, "title": "Nominee & Spouse Details", "description": "Provide spouse Aadhaar and nominee details for seamless legacy transfer."},
            {"step_number": 4, "title": "Receive PRAN (Permanent Retirement Account Number)", "description": "Get your APY PRAN card via SMS and download e-PRAN from Protean/CRA portal."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://npscra.nsdl.co.in/scheme-details.php",
        "india_gov_url": "https://www.india.gov.in/spotlight/atal-pension-yojana",
        "helpline": "1800-110-069 / 022-24993499",
        "faq": [
            {"question": "What happens if a subscriber dies before 60?", "answer": "The spouse can either continue contributing to the account for the remaining tenure or opt to receive the full accumulated corpus."}
        ],
        "tags": ["pension", "retirement", "social security", "guaranteed income", "central"],
        "featured": True
    },
    {
        "id": "pm-jeevan-jyoti-bima",
        "title": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
        "title_hi": "प्रधानमंत्री जीवन ज्योति बीमा योजना (पीएमजेजेबीवाई)",
        "short_name": "PM Jeevan Jyoti Life Insurance",
        "ministry": "Ministry of Finance",
        "sector": "Social Security",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "One-year life insurance scheme renewable from year to year, offering ₹2,00,000 life insurance cover for death due to any reason at a nominal premium of just ₹436 per annum via auto-debit from bank account.",
        "benefit_summary": "₹2,00,000 Life risk cover for just ₹436 per year (₹1.20 per day)",
        "benefit_type": "Health Coverage",
        "max_financial_benefit": "₹2,00,000 Life Insurance Cover",
        "eligibility_criteria": [
            "Any Indian citizen aged between 18 and 50 years having a savings bank account",
            "Consent to join auto-debit on an annual renewal basis",
            "Coverage valid up to age 55 years"
        ],
        "target_beneficiaries": ["All Bank Account Holders", "Low-Income Families", "Daily Wage Earners"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 50,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Primary KYC", "how_to_get": "UIDAI"},
            {"name": "Bank Passbook with Auto-Debit Consent", "mandatory": True, "description": "For deducting ₹436/yr", "how_to_get": "Bank branch / Netbanking"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Enable via Netbanking / Mobile Banking", "description": "Open your mobile banking app, navigate to 'Social Security Schemes' and select PMJJBY."},
            {"step_number": 2, "title": "Confirm Auto-Debit & Nominee", "description": "Confirm deduction of ₹436 from savings account and enter nominee details."},
            {"step_number": 3, "title": "Instant Policy Certificate", "description": "Download insurance policy certificate with coverage from June 1 to May 31."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://financialservices.gov.in/beta/en/schemes-and-services/pmjjby",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-jeevan-jyoti-bima-yojana",
        "helpline": "1800-180-1111 / 1800-110-001",
        "faq": [
            {"question": "Does it cover natural death as well as accidental death?", "answer": "Yes, PMJJBY covers death due to any cause (natural, illness, or accident)."}
        ],
        "tags": ["insurance", "life insurance", "social security", "central"],
        "featured": False
    },
    {
        "id": "pm-suraksha-bima",
        "title": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
        "title_hi": "प्रधानमंत्री सुरक्षा बीमा योजना (पीएमएसबीवाई)",
        "short_name": "PM Suraksha Accident Insurance",
        "ministry": "Ministry of Finance",
        "sector": "Social Security",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "India's most affordable accidental death and disability insurance policy, providing ₹2,00,000 for accidental death or total permanent disability, and ₹1,00,000 for partial permanent disability at an ultra-low premium of just ₹20 per year.",
        "benefit_summary": "₹2,00,000 Accidental death/full disability cover for only ₹20 per year",
        "benefit_type": "Health Coverage",
        "max_financial_benefit": "₹2,00,000 Accidental Cover",
        "eligibility_criteria": [
            "Individuals aged between 18 and 70 years having a bank account",
            "Auto-debit authorization of ₹20 annually"
        ],
        "target_beneficiaries": ["All Bank Account Holders", "Drivers", "Construction Workers", "Laborers"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 70,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "KYC verification", "how_to_get": "UIDAI"},
            {"name": "Bank Passbook", "mandatory": True, "description": "Account for ₹20 auto-debit", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Enroll via SMS or Netbanking", "description": "Send SMS 'PMSBY Y' from registered mobile to bank code or enroll through Netbanking."},
            {"step_number": 2, "title": "Submit Nominee Details", "description": "Specify nominee relationship and Aadhaar number."},
            {"step_number": 3, "title": "Policy Activation", "description": "₹20 is debited automatically every year in May."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://financialservices.gov.in/beta/en/schemes-and-services/pmsby",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-suraksha-bima-yojana",
        "helpline": "1800-180-1111",
        "faq": [
            {"question": "What is the compensation for loss of one eye or one hand?", "answer": "₹1,00,000 is paid for irrecoverable loss of one eye or loss of use of one hand or foot."}
        ],
        "tags": ["accident insurance", "social security", "low cost", "central"],
        "featured": False
    },
    {
        "id": "pmkvy-skills",
        "title": "Pradhan Mantri Kaushal Vikas Yojana 4.0 (PMKVY)",
        "title_hi": "प्रधानमंत्री कौशल विकास योजना 4.0 (पीएमकेवीवाई)",
        "short_name": "PMKVY Skill India",
        "ministry": "Ministry of Skill Development and Entrepreneurship",
        "sector": "Education & Skills",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Skill India flagship initiative providing free industry-aligned technical skill training, National Skill Qualification Framework (NSQF) certification, on-job training (OJT), digital literacy, and monetary rewards/stipends to school/college dropouts and unemployed youth across futuristic sectors like AI, Drone tech, Robotics, EV servicing, Solar, and Healthcare.",
        "benefit_summary": "100% Free technical skill certification + ₹500 - ₹1,500 assessment reward + Placement assistance",
        "benefit_type": "Free Training & Certification",
        "max_financial_benefit": "Free Certified Training + Stipend & Job Support",
        "eligibility_criteria": [
            "Any Indian citizen aged between 15 and 45 years",
            "School / college dropouts or unemployed youth seeking market-relevant job skills",
            "Aadhaar card and valid bank account for reward disbursement"
        ],
        "target_beneficiaries": ["Unemployed Youth", "College Dropouts", "Rural & Urban Jobseekers", "Women"],
        "eligibility_rules": {
            "min_age": 15,
            "max_age": 45,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Student", "Unemployed / Jobseeker", "Daily Wage Laborer / Construction Worker"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Candidate identity and biometric attendance", "how_to_get": "UIDAI"},
            {"name": "Educational Marksheet (10th / 12th / ITI)", "mandatory": True, "description": "Proof of highest education qualification", "how_to_get": "School/Board/University"},
            {"name": "Bank Passbook", "mandatory": True, "description": "For direct credit of training stipend & assessment award", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on Skill India Digital Portal", "description": "Visit https://www.skillindiadigital.gov.in and create a candidate profile."},
            {"step_number": 2, "title": "Choose Sector & Course", "description": "Browse 400+ NSQF courses (e.g. Solar Panel Technician, Drone Operator, Electric Vehicle Assembly)."},
            {"step_number": 3, "title": "Enroll in Nearest Pradhan Mantri Kaushal Kendra (PMKK)", "description": "Attend free practical classroom and lab training."},
            {"step_number": 4, "title": "Pass Assessment & Get NSDC Certificate", "description": "Receive government recognized digital badge, certificate, and attend Rozgar Melas for campus placements."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.skillindiadigital.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-kaushal-vikas-yojana-pmkvy",
        "helpline": "088000-55555 / 1800-123-9626",
        "faq": [
            {"question": "Do I have to pay any fee for PMKVY training?", "answer": "No, PMKVY 4.0 courses are 100% government-funded and completely free of cost for all candidates."}
        ],
        "tags": ["skill development", "training", "youth", "certification", "jobs", "central"],
        "featured": True
    },
    {
        "id": "post-matric-scholarship-sc-st-obc",
        "title": "National Post-Matric Scholarship for SC, ST & OBC Students",
        "title_hi": "अनुसूचित जाति/जनजाति एवं अन्य पिछड़ा वर्ग के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "short_name": "Post-Matric Scholarship",
        "ministry": "Ministry of Social Justice and Empowerment",
        "sector": "Education & Skills",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Centrally sponsored scholarship scheme providing 100% non-refundable compulsory fees (tuition, exam, library, sports) and monthly maintenance allowances (up to ₹13,500 per year) directly to SC, ST, and OBC students pursuing Class 11, 12, ITI, Polytechnic, Degree, PG, Medical, and Engineering courses.",
        "benefit_summary": "100% Tuition fee waiver + up to ₹13,500/yr maintenance allowance directly into bank account",
        "benefit_type": "Scholarship / Educational Aid",
        "max_financial_benefit": "100% College Fees + ₹13,500/year Allowance",
        "eligibility_criteria": [
            "Students belonging to SC, ST, or OBC / EBC categories",
            "Pursuing recognized post-matriculation or post-secondary courses in government or accredited private institutions",
            "Annual family income must not exceed ₹2,50,000 for SC/ST and ₹1,50,000 - ₹2,50,000 for OBC students"
        ],
        "target_beneficiaries": ["SC Students", "ST Students", "OBC Students", "College/University Students"],
        "eligibility_rules": {
            "min_age": 15,
            "max_age": 35,
            "genders": ["any"],
            "categories": ["SC", "ST", "OBC", "EWS"],
            "occupations": ["Student"],
            "max_annual_income": 250000,
            "student_levels": ["Post-Matric", "Undergraduate", "Postgraduate", "Vocational/ITI"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Caste Certificate", "mandatory": True, "description": "Digitally verified SC/ST/OBC certificate from competent revenue authority", "how_to_get": "State e-District / Tehsildar office"},
            {"name": "Income Certificate", "mandatory": True, "description": "Current financial year family income below ₹2.5 Lakhs", "how_to_get": "Tehsildar / Revenue department"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Student identity linked with bank account", "how_to_get": "UIDAI"},
            {"name": "College Admission Fee Receipt & Bonafide Certificate", "mandatory": True, "description": "Proof of current year enrollment and fee structure", "how_to_get": "College administrative office"},
            {"name": "Previous Year Marksheet", "mandatory": True, "description": "Proof of passing previous qualifying examination", "how_to_get": "School/College"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on National Scholarship Portal (NSP)", "description": "Visit https://scholarships.gov.in and generate One-Time Registration (OTR) with Aadhaar Face/OTP."},
            {"step_number": 2, "title": "Fill Post-Matric Scholarship Form", "description": "Enter Institute AISHE code, course roll number, category, and fee details."},
            {"step_number": 3, "title": "Institute Level Verification", "description": "College Nodal Officer (INO) verifies student credentials online."},
            {"step_number": 4, "title": "District/State Approval & DBT Credit", "description": "Disbursement via PFMS directly to student's Aadhaar-seeded bank account."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://scholarships.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/national-scholarship-portal",
        "helpline": "0120-6619540",
        "faq": [
            {"question": "Can private college students apply?", "answer": "Yes, provided the course and college are recognized by UGC/AICTE/State Regulatory Council."}
        ],
        "tags": ["scholarship", "sc", "st", "obc", "higher education", "central"],
        "featured": True
    },
    {
        "id": "pm-fasal-bima",
        "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "title_hi": "प्रधानमंत्री फसल बीमा योजना (पीएमएफबीवाई)",
        "short_name": "PM Fasal Bima",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "sector": "Agriculture",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Comprehensive crop insurance scheme protecting farmers against non-preventable natural risks (drought, flood, cyclone, hailstorm, pest attack, post-harvest losses) at an ultra-subsidized uniform premium of only 2% for Kharif crops, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops, with remaining subsidy shared by Central and State Governments.",
        "benefit_summary": "100% Crop loss compensation against natural calamities with uniform 1.5% - 2% low farmer premium",
        "benefit_type": "Health Coverage",
        "max_financial_benefit": "Full Sum Insured based on Scale of Finance (Up to ₹50,000 - ₹1,50,000/hectare)",
        "eligibility_criteria": [
            "All farmers growing notified crops in notified areas including sharecroppers and tenant farmers",
            "Mandatory enrollment for Loanee farmers (can opt out) and voluntary for non-loanee farmers",
            "Crop sowing certificate and land ownership or tenancy agreement required"
        ],
        "target_beneficiaries": ["All Farmers", "Tenant Farmers", "Sharecroppers"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Farmer / Agriculture", "Fisherfolk / Dairy Farmer"],
            "requires_land": True,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Land Record (RoR / 7-12 / Khatauni)", "mandatory": True, "description": "Proof of land ownership or registered tenancy agreement", "how_to_get": "State Revenue portal"},
            {"name": "Sowing Certificate / Girdawari", "mandatory": True, "description": "Proof of crop sown in current season", "how_to_get": "Patwari / Village Agriculture Assistant"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Farmer identity verification", "how_to_get": "UIDAI"},
            {"name": "Bank Passbook", "mandatory": True, "description": "For claim payout settlement", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Check Cut-Off Dates & Notified Crops", "description": "Visit https://pmfby.gov.in before the cutoff date (usually July 31 for Kharif, Dec 31 for Rabi)."},
            {"step_number": 2, "title": "Calculate Premium", "description": "Use online premium calculator to see the exact 1.5% - 2% payable amount."},
            {"step_number": 3, "title": "Apply Online / Nearest CSC / Bank", "description": "Fill plot survey numbers, crop name, and pay farmer share of premium."},
            {"step_number": 4, "title": "Report Crop Damage within 72 Hours", "description": "In case of localized disaster, report loss on the Crop Insurance App or toll-free number within 72 hours for surveyor assessment."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://pmfby.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-fasal-bima-yojana",
        "helpline": "14447 / 1800-180-1551",
        "faq": [
            {"question": "How quickly must localized crop loss be reported?", "answer": "Within 72 hours of occurrence through the Crop Insurance App, CSC center, or toll-free helpline 14447."}
        ],
        "tags": ["crop insurance", "farmer", "agriculture", "natural disaster", "central"],
        "featured": True
    },
    {
        "id": "kisan-credit-card",
        "title": "Kisan Credit Card (KCC) Scheme",
        "title_hi": "किसान क्रेडिट कार्ड (केसीसी) योजना",
        "short_name": "Kisan Credit Card",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "sector": "Agriculture",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Provides timely and hassle-free institutional credit up to ₹3,00,000 to farmers for crop cultivation, post-harvest expenses, farm maintenance, dairy, poultry, and fisheries at an effective subsidized interest rate of just 4% per annum (7% normal interest minus 3% prompt repayment incentive).",
        "benefit_summary": "Subsidized farm credit up to ₹3 Lakhs @ 4% interest with flexible revolving credit facility",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "Up to ₹3,00,000 Credit Limit @ 4% Interest",
        "eligibility_criteria": [
            "All owner cultivators, tenant farmers, oral lessees, and sharecroppers",
            "Self Help Groups (SHGs) or Joint Liability Groups (JLGs) of farmers",
            "Farmers engaged in animal husbandry, dairy, fisheries, and poultry"
        ],
        "target_beneficiaries": ["Small & Marginal Farmers", "Dairy Farmers", "Fishermen", "Tenant Farmers"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 75,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Farmer / Agriculture", "Fisherfolk / Dairy Farmer"],
            "requires_land": False,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card & PAN Card", "mandatory": True, "description": "Identity verification", "how_to_get": "UIDAI / IT Dept"},
            {"name": "Land Record (7/12, Khatauni) or Tenancy Proof", "mandatory": True, "description": "Proof of agricultural holding or livestock ownership", "how_to_get": "Revenue Patwari"},
            {"name": "Crop Sowing Pattern / Livestock Certificate", "mandatory": True, "description": "Scale of finance computation", "how_to_get": "Local Agriculture Officer"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Download KCC Form", "description": "Download 1-page simplified KCC form from https://pmkisan.gov.in or bank portal."},
            {"step_number": 2, "title": "Submit at Bank Branch or CSC", "description": "Submit at your commercial, regional rural, or cooperative bank branch."},
            {"step_number": 3, "title": "Credit Limit Sanction & Card Issuance", "description": "Bank assesses limit within 14 days and issues RuPay KCC card for ATM/POS withdrawals."}
        ],
        "application_mode": "Hybrid",
        "official_portal_url": "https://www.myscheme.gov.in/schemes/kcc",
        "india_gov_url": "https://www.india.gov.in/kisan-credit-card-scheme",
        "helpline": "1800-115-526 / 011-24300606",
        "faq": [
            {"question": "What is the collateral limit for KCC?", "answer": "No collateral is required for KCC loans up to ₹1,60,000 (extended up to ₹2,00,000 for tie-up arrangements)."}
        ],
        "tags": ["kcc", "crop loan", "farmer", "low interest", "central"],
        "featured": False
    },
    {
        "id": "pm-ujjwala-yojana",
        "title": "Pradhan Mantri Ujjwala Yojana 2.0 (PMUY)",
        "title_hi": "प्रधानमंत्री उज्ज्वला योजना 2.0 (पीएमयूवाई)",
        "short_name": "PM Ujjwala Free LPG",
        "ministry": "Ministry of Petroleum and Natural Gas",
        "sector": "Housing & Sanitation",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Provides deposit-free LPG connections to poor adult women from low-income households. Includes free first refill cylinder, free double-burner stove, and a sustained subsidy of ₹300 per refill directly credited via DBT to promote clean cooking fuel and protect respiratory health.",
        "benefit_summary": "100% Free deposit-free LPG connection + Free first cylinder + Free gas stove + ₹300 subsidy per cylinder",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "Free Connection & Kit + ₹300 Subsidy/Refill",
        "eligibility_criteria": [
            "Applicant must be an adult woman (aged 18+) from a poor household",
            "Household must not possess an existing active LPG connection from any OMC",
            "Belonging to SC/ST, PMAY beneficiaries, Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea tribes, or poor households under 14-point declaration"
        ],
        "target_beneficiaries": ["Rural Women", "Low-Income Families", "BPL/Ration Card Holders", "SC/ST"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["All"],
            "max_annual_income": 200000,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card of Woman Applicant", "mandatory": True, "description": "Primary identity verification", "how_to_get": "UIDAI"},
            {"name": "Ration Card / Family Composition Proof", "mandatory": True, "description": "To verify non-existence of existing connection", "how_to_get": "State Food & Civil Supplies"},
            {"name": "Bank Passbook (Aadhaar Seeded)", "mandatory": True, "description": "For receiving direct cylinder subsidy (DBTL/PAHAL)", "how_to_get": "Bank branch"},
            {"name": "Address Proof / Self-Declaration for Migrants", "mandatory": True, "description": "Residence certificate or migrant declaration form", "how_to_get": "Panchayat / Self-signed"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply Online or at LPG Distributor", "description": "Visit https://www.pmuy.gov.in or nearest Indane, Bharatgas, or HP Gas dealership."},
            {"step_number": 2, "title": "Submit Aadhaar & Family Details", "description": "Fill Ujjwala 2.0 application form and submit Aadhaar KYC for adult family members."},
            {"step_number": 3, "title": "De-Duplication Check", "description": "Oil Marketing Companies (OMCs) run electronic NIC check to confirm no prior connection."},
            {"step_number": 4, "title": "Collect Free Gas Cylinder & Stove", "description": "Receive free 14.2kg filled cylinder, regulator, safety hose, and 2-burner stove at zero cost."}
        ],
        "application_mode": "Hybrid",
        "official_portal_url": "https://www.pmuy.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-ujjwala-yojana",
        "helpline": "1800-266-6696 / 1906 (Emergency)",
        "faq": [
            {"question": "Can migrant workers apply without local address proof?", "answer": "Yes, under Ujjwala 2.0, migrants can simply submit a self-declaration for proof of address and family composition."}
        ],
        "tags": ["ujjwala", "lpg", "women", "clean energy", "free stove", "central"],
        "featured": True
    },
    {
        "id": "pm-surya-ghar-muft-bijli",
        "title": "PM Surya Ghar: Muft Bijli Yojana",
        "title_hi": "पीएम सूर्य घर: मुफ्त बिजली योजना",
        "short_name": "PM Surya Ghar Solar",
        "ministry": "Ministry of New and Renewable Energy",
        "sector": "Housing & Sanitation",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "National rooftop solar scheme providing up to ₹78,000 direct capital subsidy to households for installing 1kW to 3kW grid-connected rooftop solar systems, enabling families to get up to 300 units of free electricity every month and earn revenue by selling surplus power back to the grid.",
        "benefit_summary": "Up to ₹78,000 direct bank subsidy + 300 units free electricity per month + income from surplus power",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "₹78,000 Capital Subsidy + ₹15,000/yr Power Savings",
        "eligibility_criteria": [
            "Indian residential households having a suitable roof and active grid electricity connection",
            "Electricity meter in the name of the applicant or family member",
            "Must not have availed Central Financial Assistance (CFA) for rooftop solar on the same connection earlier"
        ],
        "target_beneficiaries": ["Homeowners", "Residential Families", "Middle-Class & Low-Income Households"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Recent Electricity Bill", "mandatory": True, "description": "Consumer Account Number (CA/Consumer ID)", "how_to_get": "Power distribution company (DISCOM)"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Applicant KYC verification", "how_to_get": "UIDAI"},
            {"name": "Bank Passbook / Cancelled Cheque", "mandatory": True, "description": "Account where ₹78k subsidy will be credited directly", "how_to_get": "Bank branch"},
            {"name": "Photograph of Rooftop", "mandatory": True, "description": "Proof of shadow-free rooftop space", "how_to_get": "Smartphone photo"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on National Solar Portal", "description": "Visit https://pmsuryaghar.gov.in, select your State and Electricity DISCOM, and enter Consumer Number."},
            {"step_number": 2, "title": "Apply for Rooftop Solar & Feasibility Approval", "description": "Submit application; DISCOM issues digital technical feasibility approval."},
            {"step_number": 3, "title": "Installation through Empaneled Vendor", "description": "Select registered vendor, execute agreement, and get net-metered solar installed."},
            {"step_number": 4, "title": "DISCOM Inspection & Direct Subsidy", "description": "DISCOM installs net-meter, generates commissioning certificate; central subsidy of ₹78,000 credited to bank within 30 days."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://pmsuryaghar.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pm-surya-ghar-muft-bijli-yojana",
        "helpline": "15555 / 1800-180-3333",
        "faq": [
            {"question": "What is the subsidy breakdown?", "answer": "1 kW system: ₹30,000; 2 kW system: ₹60,000; 3 kW and above: ₹78,000 direct bank transfer."}
        ],
        "tags": ["solar", "free electricity", "rooftop", "clean energy", "central"],
        "featured": True
    },
    {
        "id": "mgnrega-employment",
        "title": "Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA)",
        "title_hi": "महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी अधिनियम (मनरेगा)",
        "short_name": "MGNREGA 100-Day Wage",
        "ministry": "Ministry of Rural Development",
        "sector": "Social Security",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "World's largest legal social security guarantee, providing at least 100 days of guaranteed wage employment in every financial year to every rural household whose adult members volunteer to do unskilled manual work at notified statutory daily wage rates (₹240 - ₹374/day depending on state).",
        "benefit_summary": "100 Days guaranteed wage employment per year (₹240 - ₹374/day) + Unemployment allowance if work not given in 15 days",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹24,000 - ₹37,000 / year guaranteed wages",
        "eligibility_criteria": [
            "Adult members of rural households willing to do unskilled manual labor",
            "Must reside in rural Gram Panchayat area",
            "Holding a valid MGNREGA Job Card"
        ],
        "target_beneficiaries": ["Rural Laborers", "Small Farmers", "Agricultural Workers", "Women Workers"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 70,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Daily Wage Laborer / Construction Worker", "Farmer / Agriculture", "Unemployed / Jobseeker"],
            "area_type": "rural"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "ABPS (Aadhaar-Based Payment System) verification", "how_to_get": "UIDAI"},
            {"name": "MGNREGA Job Card", "mandatory": True, "description": "Issued free by Gram Panchayat", "how_to_get": "Gram Rozgar Sahayak / Panchayat Secretary"},
            {"name": "Bank / Post Office Account Passbook", "mandatory": True, "description": "For weekly wage credits", "how_to_get": "Bank branch / Post Office"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply for Job Card at Gram Panchayat", "description": "Submit application with family photographs to Panchayat Secretary."},
            {"step_number": 2, "title": "Receive Job Card within 15 Days", "description": "Gram Panchayat issues laminated Job Card free of cost."},
            {"step_number": 3, "title": "Demand Work (Form 4)", "description": "Submit written request for work to Gram Rozgar Sahayak indicating start date."},
            {"step_number": 4, "title": "Allotment of Work within 5km", "description": "Work allocated within 15 days, else entitled to statutory daily unemployment allowance."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://nrega.nic.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/mahatma-gandhi-national-rural-employment-guarantee-act",
        "helpline": "1800-345-6565 / 1800-11-0707",
        "faq": [
            {"question": "How soon are wages paid?", "answer": "Statutorily within 15 days of muster roll closure directly into worker's Aadhaar-linked bank account."}
        ],
        "tags": ["mgnrega", "employment", "wage labor", "rural", "central"],
        "featured": True
    },
    {
        "id": "pm-egp-subsidy",
        "title": "Prime Minister's Employment Generation Programme (PMEGP)",
        "title_hi": "प्रधानमंत्री रोजगार सृजन कार्यक्रम (पीएमईजीपी)",
        "short_name": "PMEGP Business Subsidy",
        "ministry": "Ministry of Micro, Small and Medium Enterprises",
        "sector": "Employment & MSME",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Credit-linked subsidy program to generate self-employment ventures. Provides 15% to 35% government capital subsidy on bank-financed manufacturing projects up to ₹50 Lakhs and service sector projects up to ₹20 Lakhs.",
        "benefit_summary": "15% to 35% non-refundable government margin money subsidy on project costs up to ₹50 Lakhs",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "Up to ₹17.5 Lakhs Government Subsidy (35% on ₹50L)",
        "eligibility_criteria": [
            "Any individual above 18 years of age with at least 8th standard pass for projects above ₹10L (manufacturing) and ₹5L (service)",
            "Self Help Groups, Production Co-operative Societies, and Registered Trusts",
            "Existing units or units that have availed other central/state subsidy are not eligible"
        ],
        "target_beneficiaries": ["Unemployed Youth", "First-Time Entrepreneurs", "Women", "SC/ST/OBC/Minorities/Ex-Servicemen/PwD"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 60,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Self-Employed / Micro Business", "Unemployed / Jobseeker", "Artisan / Craftsman (Vishwakarma)"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Detailed Project Report (DPR)", "mandatory": True, "description": "Business plan with cost breakdown and feasibility", "how_to_get": "Prepared via KVIC templates or Chartered Accountant"},
            {"name": "Aadhaar Card & PAN", "mandatory": True, "description": "Identity and tax proof", "how_to_get": "UIDAI / IT Dept"},
            {"name": "Educational Marksheet (8th / 10th / Degree)", "mandatory": True, "description": "Proof of basic educational qualification", "how_to_get": "School/Board"},
            {"name": "Special Category Certificate (Caste/PwD/Ex-Servicemen)", "mandatory": False, "description": "To claim higher 25%-35% subsidy rate", "how_to_get": "Competent authority"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply on PMEGP e-Portal", "description": "Visit https://www.kviconline.gov.in/pmegpeportal and select individual application."},
            {"step_number": 2, "title": "Fill Sponsoring Agency & Financing Bank", "description": "Choose KVIC, KVIB, or DIC as sponsoring agency and preferred bank branch."},
            {"step_number": 3, "title": "District Level Task Force Screening", "description": "DLTFC screens project proposal and forwards to bank for credit sanction."},
            {"step_number": 4, "title": "EDP Training & Margin Money Credit", "description": "Undergo 10-day Entrepreneurship Development Programme (EDP) training and receive margin money locked in term deposit."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.kviconline.gov.in/pmegpeportal",
        "india_gov_url": "https://www.india.gov.in/prime-ministers-employment-generation-programme-pmegp",
        "helpline": "1800-3000-0034 / 022-26711003",
        "faq": [
            {"question": "What is the subsidy percentage for rural women and SC/ST?", "answer": "35% of project cost in rural areas and 25% in urban areas with only 5% beneficiary own contribution."}
        ],
        "tags": ["pmegp", "startup", "manufacturing", "subsidy", "msme", "central"],
        "featured": True
    },
    {
        "id": "adip-disability-aids",
        "title": "Assistance to Disabled Persons for Purchase of Aids and Appliances (ADIP)",
        "title_hi": "दिव्यांगजनों को सहायक उपकरण खरीदने हेतु सहायता (एडिप योजना)",
        "short_name": "ADIP Divyangjan Aids",
        "ministry": "Ministry of Social Justice and Empowerment",
        "sector": "Social Security",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Provides 100% free modern, high-quality, scientifically manufactured assistive aids and appliances (motorized tricycles, smart canes, digital hearing aids, battery wheelchairs, prosthetic limbs, braille laptops) to persons with disabilities (Divyangjan) to promote physical, social, and economic independence.",
        "benefit_summary": "100% Free modern assistive equipment (Motorized tricycles, wheelchairs, smart hearing aids, prosthetics)",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "Free Assistive Devices (Value up to ₹50,000+)",
        "eligibility_criteria": [
            "Indian citizen of any age holding a benchmark disability certificate of 40% or more (UDID Card)",
            "Monthly income of family/individual from all sources not exceeding ₹30,000 per month (100% free aid for income up to ₹22,500/mo, 50% aid for ₹22,501 to ₹30,000/mo)",
            "Has not received the same aid/appliance from government in last 3 years (1 year for children below 12)"
        ],
        "target_beneficiaries": ["Specially Abled Persons", "Divyangjan", "Children with Special Needs", "Differently Abled Elders"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 90,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "requires_disability": True,
            "max_annual_income": 360000,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Disability Certificate / UDID Card", "mandatory": True, "description": "Showing 40% or more disability issued by medical board", "how_to_get": "District Civil Hospital / swavlambancard.gov.in"},
            {"name": "Income Certificate", "mandatory": True, "description": "Proof of income below ₹30,000/month", "how_to_get": "Tehsildar / Employer / BPL card"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity verification", "how_to_get": "UIDAI"},
            {"name": "Passport Sized Photograph showing Disability", "mandatory": True, "description": "Visual record of beneficiary", "how_to_get": "Photo studio"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Check ALIMCO Camp Schedule or Apply Online", "description": "Visit https://alimco.in or District Disability Rehabilitation Centre (DDRC)."},
            {"step_number": 2, "title": "Assessment by Clinical Experts", "description": "Doctors and prosthetists assess exact requirement (e.g. customized motorized tricycle or hearing frequency)."},
            {"step_number": 3, "title": "Free Distribution at Mega Camp", "description": "Collect assistive equipment completely free of charge with warranty and training."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://alimco.in",
        "india_gov_url": "https://www.india.gov.in/assistance-disabled-persons-purchasefitting-aids-and-appliances-adip-scheme",
        "helpline": "1800-180-5129 / 0512-2770137",
        "faq": [
            {"question": "Are motorized tricycles covered?", "answer": "Yes, severely locomotor disabled individuals aged 16+ with 80%+ disability and income under limit receive motorized tricycles free."}
        ],
        "tags": ["disability", "divyangjan", "assistive aids", "wheelchair", "udid", "central"],
        "featured": True
    },
    {
        "id": "rashtriya-vayoshri-yojana",
        "title": "Rashtriya Vayoshri Yojana (RVY)",
        "title_hi": "राष्ट्रीय वयोश्री योजना (आरवीवाई)",
        "short_name": "Rashtriya Vayoshri Elder Aid",
        "ministry": "Ministry of Social Justice and Empowerment",
        "sector": "Social Security",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Scheme for providing physical aids and assisted-living devices (walking sticks, elbow crutches, quadpods, tripod walking sticks, hearing aids, wheelchairs, artificial dentures, spectacles) for Senior Citizens belonging to BPL category suffering from age-related disabilities and infirmities.",
        "benefit_summary": "100% Free spectacles, dentures, hearing aids, wheelchairs, and walking frames for senior citizens",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "Free Assisted-Living Equipment (Value up to ₹15,000+)",
        "eligibility_criteria": [
            "Senior citizen aged 60 years and above",
            "Must possess a BPL / Antyodaya Ration Card or have monthly income under statutory state BPL threshold",
            "Suffering from age-related disability or infirmity (low vision, hearing loss, loss of teeth, locomotor disability)"
        ],
        "target_beneficiaries": ["Senior Citizens (60+)", "BPL Elderly", "Elderly Widows"],
        "eligibility_rules": {
            "min_age": 60,
            "max_age": 100,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Senior Citizen / Retired", "All"],
            "max_annual_income": 200000,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card / Age Proof", "mandatory": True, "description": "Proof of age 60+", "how_to_get": "UIDAI / Voter ID"},
            {"name": "BPL Ration Card / Income Certificate", "mandatory": True, "description": "Proof of low-income status", "how_to_get": "Food department / Tehsildar"},
            {"name": "Medical Certificate of Disability / Infirmity", "mandatory": True, "description": "Issued by CMO or Govt Doctor at assessment camp", "how_to_get": "ALIMCO Camp Doctor"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Attend District Vayoshri Assessment Camp", "description": "District Social Welfare Officer organizes ALIMCO medical assessment camps at Block level."},
            {"step_number": 2, "title": "Clinical Examination", "description": "Eye, ENT, dental, and orthopedic doctors examine specific requirements."},
            {"step_number": 3, "title": "Free Kit Distribution", "description": "Customized devices distributed in ceremonial camps."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://socialjustice.gov.in/schemes/73",
        "india_gov_url": "https://www.india.gov.in/spotlight/rashtriya-vayoshri-yojana",
        "helpline": "14567 (Elderline) / 1800-180-5129",
        "faq": [
            {"question": "Can elderly people call for home assistance?", "answer": "Yes, National Helpline for Senior Citizens 'Elderline' on toll-free 14567 guides on upcoming camps and welfare."}
        ],
        "tags": ["senior citizen", "elderly", "hearing aid", "spectacles", "bpl", "central"],
        "featured": False
    },
    {
        "id": "ignoaps-old-age-pension",
        "title": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
        "title_hi": "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना",
        "short_name": "IGNOAPS National Pension",
        "ministry": "Ministry of Rural Development",
        "sector": "Financial Inclusion & Pension",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Under the National Social Assistance Programme (NSAP), this scheme provides non-contributory monthly cash pensions to destitute elderly persons living below the poverty line (BPL) across India, supplemented by matching state contributions.",
        "benefit_summary": "₹1,000 to ₹3,000 per month (combined central + state share) direct pension into bank account",
        "benefit_type": "Pension",
        "max_financial_benefit": "₹1,000 - ₹3,000 / month lifetime pension",
        "eligibility_criteria": [
            "Applicant must be 60 years of age or older",
            "Applicant must belong to a household living Below the Poverty Line (BPL)",
            "Valid BPL card or SECC inclusion required"
        ],
        "target_beneficiaries": ["Destitute Elderly", "BPL Senior Citizens", "Elderly Widows"],
        "eligibility_rules": {
            "min_age": 60,
            "max_age": 105,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Senior Citizen / Retired", "All"],
            "max_annual_income": 120000,
            "requires_bpl": True,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity and age proof", "how_to_get": "UIDAI"},
            {"name": "BPL / Antyodaya Ration Card", "mandatory": True, "description": "Proof of BPL status", "how_to_get": "Food & Civil Supplies"},
            {"name": "Bank / Post Office Passbook", "mandatory": True, "description": "Individual account for monthly pension DBT", "how_to_get": "Bank / Post Office"},
            {"name": "Age Verification Certificate", "mandatory": True, "description": "Medical officer age certificate if age not in birth record", "how_to_get": "District Hospital"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Submit Application at Block / Municipality", "description": "Submit NSAP Form to Block Development Officer (BDO) or Municipal Executive Officer."},
            {"step_number": 2, "title": "Verification by Social Welfare Inspector", "description": "Field verification of age and BPL status."},
            {"step_number": 3, "title": "Sanction Order & Direct Monthly DBT", "description": "Pension sanctioned and credited on the 1st week of every month via PFMS."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://nsap.nic.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/national-social-assistance-programme-nsap",
        "helpline": "1800-11-6446 / 14567",
        "faq": [
            {"question": "Does the pension amount increase after 80 years?", "answer": "Yes, central assistance increases from ₹200 to ₹500/month for seniors aged 80+, plus additional state top-ups."}
        ],
        "tags": ["pension", "bpl", "senior citizen", "nsap", "dbt", "central"],
        "featured": False
    },
    {
        "id": "pm-janaushadhi",
        "title": "Pradhan Mantri Bharatiya Janaushadhi Pariyojana (PMBJP)",
        "title_hi": "प्रधानमंत्री भारतीय जनऔषधि परियोजना (पीएमबीजेपी)",
        "short_name": "PM Jan Aushadhi Generic Medicines",
        "ministry": "Ministry of Chemicals and Fertilizers",
        "sector": "Healthcare",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Making quality medicines accessible to everyone by providing 2,047 high-standard generic medicines and 300 surgical equipment at 50% to 90% cheaper prices than branded market equivalents through 12,000+ Jan Aushadhi Kendras across India.",
        "benefit_summary": "50% to 90% discount on all essential medicines (Diabetes, BP, Cardiac, Antibiotics, Oncology, Sanitary pads @ ₹1/pad)",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "50% - 90% Savings on Monthly Medical Expenses",
        "eligibility_criteria": [
            "Open universally to all Indian citizens without any income or category restriction",
            "No prior registration needed; available with any valid doctor's prescription"
        ],
        "target_beneficiaries": ["All Citizens", "Chronic Disease Patients", "Elderly", "Low & Middle Income Families"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 100,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Doctor's Prescription", "mandatory": True, "description": "Prescription showing generic/salt or brand name", "how_to_get": "Registered Medical Practitioner"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Locate Nearest Jan Aushadhi Kendra", "description": "Download 'Jan Aushadhi Sugam' App or visit http://janaushadhi.gov.in."},
            {"step_number": 2, "title": "Present Prescription", "description": "Show prescription to pharmacist at Kendra."},
            {"step_number": 3, "title": "Purchase at 50-90% Lower Price", "description": "Get WHO-GMP certified high-grade generic medicines instantly."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "http://janaushadhi.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-bhartiya-janaushadhi-pariyojana-pmbjp",
        "helpline": "1800-180-8080",
        "faq": [
            {"question": "Are Jan Aushadhi medicines equal in quality to branded medicines?", "answer": "Yes, every batch is tested at NABL-accredited laboratories and conforms strictly to Indian Pharmacopoeia standards."}
        ],
        "tags": ["healthcare", "generic medicines", "cheap medicine", "universal", "central"],
        "featured": False
    },
    {
        "id": "stand-up-india",
        "title": "Stand-Up India Scheme for Women & SC/ST Entrepreneurs",
        "title_hi": "स्टैंड-अप इंडिया योजना (महिला एवं अनुसूचित जाति/जनजाति उद्यम)",
        "short_name": "Stand-Up India Enterprise Loan",
        "ministry": "Ministry of Finance",
        "sector": "Employment & MSME",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Facilitates bank loans between ₹10 Lakhs and ₹1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one Woman borrower per bank branch for setting up greenfield enterprises in manufacturing, services, agri-allied activities, or trading.",
        "benefit_summary": "Bank composite loan of ₹10 Lakhs to ₹1 Crore with low margin money and credit guarantee coverage",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "₹10 Lakhs - ₹1 Crore Enterprise Loan",
        "eligibility_criteria": [
            "SC/ST and/or Woman entrepreneurs above 18 years of age",
            "Loans available only for Greenfield (first-time) ventures in manufacturing, services, or trading",
            "In non-individual enterprises, at least 51% shareholding and controlling stake must be held by SC/ST or Woman entrepreneur"
        ],
        "target_beneficiaries": ["Women Entrepreneurs", "SC Entrepreneurs", "ST Entrepreneurs"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 65,
            "genders": ["female", "any"],
            "categories": ["SC", "ST", "General", "OBC", "EWS"],
            "occupations": ["Self-Employed / Micro Business", "Salaried (Private/Public)", "Unemployed / Jobseeker"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Detailed Project Report (DPR)", "mandatory": True, "description": "Project feasibility, cash flows, and machinery requirement", "how_to_get": "CA / Consultant"},
            {"name": "Aadhaar & PAN Card", "mandatory": True, "description": "KYC identity", "how_to_get": "UIDAI / IT Dept"},
            {"name": "Caste Certificate (for SC/ST)", "mandatory": False, "description": "Mandatory if claiming SC/ST quota", "how_to_get": "Tehsildar"},
            {"name": "Proof of Business Premises / Lease Agreement", "mandatory": True, "description": "Industrial/Commercial space location", "how_to_get": "Rental lease agreement"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on Stand-Up Mitra Portal", "description": "Visit https://www.standupmitra.in and fill applicant registration."},
            {"step_number": 2, "title": "Select Handholding Support or Direct Loan", "description": "Choose mentoring/technical training or direct loan application to designated bank."},
            {"step_number": 3, "title": "Bank Appraisal & Sanction", "description": "Bank assesses project and disburses composite term loan + working capital limit."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.standupmitra.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/stand-india-scheme",
        "helpline": "1800-180-1111 / 011-23748721",
        "faq": [
            {"question": "What is the margin money requirement?", "answer": "The borrower needs to bring in up to 15% of project cost, which can also be converged with eligible state/central subsidies."}
        ],
        "tags": ["stand up india", "women entrepreneur", "sc st loan", "msme", "central"],
        "featured": True
    },
    {
        "id": "mahila-samman-savings",
        "title": "Mahila Samman Savings Certificate (MSSC)",
        "title_hi": "महिला सम्मान बचत प्रमाण पत्र (एमएसएससी)",
        "short_name": "Mahila Samman Certificate",
        "ministry": "Ministry of Finance",
        "sector": "Women & Child",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Exclusive one-time small savings scheme for women and girls offering high guaranteed 7.5% fixed interest per annum compounded quarterly for a 2-year tenure, with deposit limits from ₹1,000 up to ₹2,00,000 and 40% partial withdrawal facility after 1 year.",
        "benefit_summary": "7.5% Guaranteed fixed interest for women & girls on 2-year deposits up to ₹2 Lakhs",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "7.5% Annual Compounded Interest",
        "eligibility_criteria": [
            "Account can be opened by a woman for herself, or by guardian on behalf of a minor girl child",
            "Tenure of 2 years from date of deposit",
            "Maximum investment ceiling of ₹2 Lakhs per individual across all accounts"
        ],
        "target_beneficiaries": ["Women", "Girls", "Homemakers", "Working Women"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 90,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity and KYC verification", "how_to_get": "UIDAI"},
            {"name": "PAN Card", "mandatory": True, "description": "Tax and financial KYC", "how_to_get": "IT Dept"},
            {"name": "Passport Sized Photographs", "mandatory": True, "description": "Applicant photo", "how_to_get": "Studio"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Visit Post Office or Authorized Bank", "description": "Available at all Head/Sub Post Offices and banks (SBI, Canara, BoB, Union Bank, etc.)."},
            {"step_number": 2, "title": "Submit Form-1 with KYC", "description": "Submit account opening form along with deposit amount (cheque/cash)."},
            {"step_number": 3, "title": "Receive MSSC Certificate & Passbook", "description": "Get physical passbook showing maturity amount with 7.5% interest."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://www.indiapost.gov.in/Financial/Pages/Content/Mahila-Samman-Savings-Certificate.aspx",
        "india_gov_url": "https://www.india.gov.in/mahila-samman-savings-certificate-2023",
        "helpline": "1800-266-6868",
        "faq": [
            {"question": "Can I withdraw money before 2 years?", "answer": "Yes, up to 40% of the balance can be withdrawn after 1 year from the date of account opening."}
        ],
        "tags": ["women", "savings", "fixed return", "safe investment", "central"],
        "featured": False
    },
    {
        "id": "pragati-scholarship-girls",
        "title": "AICTE Pragati Scholarship Scheme for Girl Students",
        "title_hi": "एआईसीटीई प्रगति छात्रवृत्ति योजना (बालिकाओं के लिए)",
        "short_name": "Pragati Girl Tech Scholarship",
        "ministry": "Ministry of Education",
        "sector": "Education & Skills",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Empowers young women pursuing higher technical education (Technical Degree or Diploma in Engineering, Architecture, Pharmacy, etc.) in AICTE approved institutions by providing ₹50,000 per annum for all years of study towards tuition fees, laptop, books, and stationeries.",
        "benefit_summary": "₹50,000 per year scholarship for girl students in engineering, architecture, and diploma colleges",
        "benefit_type": "Scholarship / Educational Aid",
        "max_financial_benefit": "₹50,000 / year for entire course duration",
        "eligibility_criteria": [
            "Girl candidate admitted to 1st year of Degree/Diploma course or 2nd year through lateral entry in AICTE approved institution",
            "Maximum 2 girl children per family eligible",
            "Family annual income must not exceed ₹8,00,000"
        ],
        "target_beneficiaries": ["Girl Students in Engineering / Polytechnic / Pharmacy"],
        "eligibility_rules": {
            "min_age": 16,
            "max_age": 30,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["Student"],
            "max_annual_income": 800000,
            "student_levels": ["Undergraduate", "Vocational/ITI"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Class 10th & 12th Marksheets", "mandatory": True, "description": "Proof of academic qualification", "how_to_get": "Board of Education"},
            {"name": "College Admission Fee Receipt & Bonafide", "mandatory": True, "description": "Proof of admission in AICTE approved college", "how_to_get": "College Principal office"},
            {"name": "Family Income Certificate (below ₹8L)", "mandatory": True, "description": "Issued by Tehsildar/competent authority", "how_to_get": "State Revenue Department"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Student identity linked with bank account", "how_to_get": "UIDAI"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply on National Scholarship Portal", "description": "Visit https://scholarships.gov.in and choose AICTE Pragati Scholarship."},
            {"step_number": 2, "title": "Enter College & Academic Details", "description": "Provide Centralized Admission Process (CAP) allotment letter and college roll number."},
            {"step_number": 3, "title": "College & AICTE Verification", "description": "College verifies documents; ₹50,000 credited annually via DBT."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.aicte-india.org/schemes/students-development-schemes/pragati-scholarship-scheme",
        "india_gov_url": "https://www.india.gov.in/pragati-scholarship-scheme-girl-child",
        "helpline": "011-29581000",
        "faq": [
            {"question": "How many scholarships are awarded each year?", "answer": "10,000 scholarships are awarded every year across Degree and Diploma streams."}
        ],
        "tags": ["girls", "scholarship", "engineering", "technical education", "central"],
        "featured": True
    },
    {
        "id": "ladli-behna-mp",
        "title": "Mukhyamantri Ladli Behna Yojana (Madhya Pradesh)",
        "title_hi": "मुख्यमंत्री लाड़ली बहना योजना (मध्य प्रदेश)",
        "short_name": "MP Ladli Behna",
        "ministry": "Women & Child Development Department, Govt of Madhya Pradesh",
        "sector": "Women & Child",
        "is_central": False,
        "applicable_states": ["Madhya Pradesh"],
        "description": "Pioneering state welfare scheme by the Government of Madhya Pradesh providing direct monthly financial assistance of ₹1,250 (₹15,000 per year) directly into the Aadhaar-linked bank accounts of eligible resident women to foster economic independence, nutrition, and health.",
        "benefit_summary": "₹1,250 per month (₹15,000/yr) direct cash transfer into bank account on 10th of every month",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹15,000 / year DBT",
        "eligibility_criteria": [
            "Permanent resident woman of Madhya Pradesh",
            "Age between 21 and 60 years on January 1 of calendar year",
            "Married, widowed, divorced, or abandoned women",
            "Combined family annual income must not exceed ₹2,50,000 and family must not own more than 5 acres of agricultural land"
        ],
        "target_beneficiaries": ["Women of MP", "Homemakers", "Rural & Urban Poor Women"],
        "eligibility_rules": {
            "min_age": 21,
            "max_age": 60,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["All"],
            "max_annual_income": 250000,
            "state_restriction": ["Madhya Pradesh"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Samagra Family ID & Member ID", "mandatory": True, "description": "MP Samagra Portal 9-digit eKYC verified ID", "how_to_get": "samagra.gov.in or Gram Panchayat"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Linked with mobile and bank account", "how_to_get": "UIDAI"},
            {"name": "Aadhaar-Linked Active Bank Account Passbook", "mandatory": True, "description": "With DBT / NPCI mapper active", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Complete Samagra eKYC", "description": "Ensure your Samagra ID is linked with Aadhaar OTP/Biometric on samagra.gov.in."},
            {"step_number": 2, "title": "Attend Gram Panchayat / Ward Camp", "description": "Visit village camp; portal entry done by camp operator with live photo capture."},
            {"step_number": 3, "title": "Receive Application Slip", "description": "Get printed receipt with unique application ID."},
            {"step_number": 4, "title": "Monthly ₹1,250 Transfer", "description": "Credited directly on the 10th of every month via DBT."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://cmladlibahna.mp.gov.in",
        "india_gov_url": "https://www.india.gov.in/mukhyamantri-ladli-bahna-yojana-madhya-pradesh",
        "helpline": "0755-2700800",
        "faq": [
            {"question": "Can unmarried women apply?", "answer": "Currently, the scheme is for married, widowed, divorced, and separated women aged 21 to 60."}
        ],
        "tags": ["madhya pradesh", "women", "dbt", "cash", "state scheme"],
        "featured": True
    },
    {
        "id": "gruha-lakshmi-karnataka",
        "title": "Gruha Lakshmi Scheme (Karnataka Guarantee)",
        "title_hi": "गृह लक्ष्मी योजना (कर्नाटक)",
        "short_name": "Karnataka Gruha Lakshmi",
        "ministry": "Department of Women and Child Development, Govt of Karnataka",
        "sector": "Women & Child",
        "is_central": False,
        "applicable_states": ["Karnataka"],
        "description": "Flagship guarantee scheme by Government of Karnataka transferring ₹2,000 per month (₹24,000/yr) directly to the bank account of the designated woman head of household of Antyodaya, BPL, and APL ration card families across Karnataka.",
        "benefit_summary": "₹2,000 per month (₹24,000 per year) direct bank assistance to female head of family",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹24,000 / year DBT",
        "eligibility_criteria": [
            "Woman registered as the head of family in Karnataka Ration Card (APL, BPL, or Antyodaya)",
            "Applicant or spouse must not be an income tax payer or GST filer",
            "Permanent resident of Karnataka"
        ],
        "target_beneficiaries": ["Women Head of Households in Karnataka"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 85,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["All"],
            "max_annual_income": 300000,
            "state_restriction": ["Karnataka"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Ration Card (APL / BPL / AAY)", "mandatory": True, "description": "Showing applicant as female family head", "how_to_get": "Karnataka Ahara portal"},
            {"name": "Aadhaar Card of Woman & Husband", "mandatory": True, "description": "Identity proof", "how_to_get": "UIDAI"},
            {"name": "Aadhaar Seeded Bank Account", "mandatory": True, "description": "For direct monthly ₹2,000 credit", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Check SMS / Visit Seva Sindhu Bapuji Seva Kendra", "description": "Visit nearest Grama One, Karnataka One, or Bangalore One center."},
            {"step_number": 2, "title": "Provide Ration Card & Aadhaar", "description": "Operator verifies details on Seva Sindhu portal."},
            {"step_number": 3, "title": "Instant Acknowledgment & Monthly Credit", "description": "Receive printed acknowledgment and monthly DBT payout."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://sevasindhugs.karnataka.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/gruha-lakshmi-scheme-karnataka",
        "helpline": "1902 / 080-22279954",
        "faq": [
            {"question": "Can APL ration card holders get ₹2,000/month?", "answer": "Yes, both APL and BPL/AAY card holders qualify as long as they are not income tax/GST payers."}
        ],
        "tags": ["karnataka", "women", "dbt", "cash", "state scheme"],
        "featured": True
    },
    {
        "id": "yuva-nidhi-karnataka",
        "title": "Yuva Nidhi Scheme (Karnataka)",
        "title_hi": "युवा निधि योजना (कर्नाटक)",
        "short_name": "Karnataka Yuva Nidhi",
        "ministry": "Department of Skill Development & Livelihood, Govt of Karnataka",
        "sector": "Education & Skills",
        "is_central": False,
        "applicable_states": ["Karnataka"],
        "description": "Monthly unemployment stipend of ₹3,000 for degree holders and ₹1,500 for diploma holders who graduated in Karnataka and remained unemployed after 6 months of graduation, provided for up to 2 years along with free skill development training.",
        "benefit_summary": "₹3,000/mo (Graduates) / ₹1,500/mo (Diploma) unemployment stipend for up to 2 years + Skill training",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹3,000 / month (up to ₹72,000 in 2 years)",
        "eligibility_criteria": [
            "Domicile of Karnataka who passed Degree or Diploma from recognized universities in Karnataka",
            "Remained unemployed for at least 6 months after passing and not pursuing higher education",
            "Not employed in private/govt sector or self-employed"
        ],
        "target_beneficiaries": ["Unemployed Graduates", "Diploma Holders in Karnataka"],
        "eligibility_rules": {
            "min_age": 20,
            "max_age": 32,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Unemployed / Jobseeker", "Student"],
            "state_restriction": ["Karnataka"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Degree / Diploma Certificate & Marksheets", "mandatory": True, "description": "Proof of passing from Karnataka university", "how_to_get": "University / Board"},
            {"name": "Karnataka Domicile / Study Certificate", "mandatory": True, "description": "Proof of minimum 6 years study in Karnataka", "how_to_get": "School/College"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity and bank seeding", "how_to_get": "UIDAI"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply on Seva Sindhu Portal", "description": "Visit https://sevasindhugs.karnataka.gov.in and click on Yuva Nidhi."},
            {"step_number": 2, "title": "Enter Degree Registration Number", "description": "Portal auto-fetches degree details from NAD (National Academic Depository)."},
            {"step_number": 3, "title": "Self-Declaration of Unemployment", "description": "Submit monthly self-declaration to receive ₹3,000/month DBT."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://sevasindhugs.karnataka.gov.in",
        "india_gov_url": "https://www.india.gov.in/yuva-nidhi-scheme-karnataka",
        "helpline": "1902 / 080-22279954",
        "faq": [
            {"question": "How long is the financial assistance provided?", "answer": "For maximum 2 years from date of enrollment or until the candidate secures employment/apprenticeship."}
        ],
        "tags": ["karnataka", "unemployed", "graduates", "stipend", "youth", "state scheme"],
        "featured": False
    },
    {
        "id": "kanyashree-prakalpa-wb",
        "title": "Kanyashree Prakalpa (West Bengal)",
        "title_hi": "कन्याश्री प्रकल्प (पश्चिम बंगाल)",
        "short_name": "WB Kanyashree",
        "ministry": "Department of Women & Child Development, Govt of West Bengal",
        "sector": "Education & Skills",
        "is_central": False,
        "applicable_states": ["West Bengal"],
        "description": "United Nations Award-winning conditional cash transfer scheme in West Bengal aiming to prevent child marriage and improve girl child schooling: K1 provides ₹1,000 annual scholarship for unmarried schoolgirls (aged 13-18), and K2 provides a one-time grant of ₹25,000 on turning 18 if unmarried and enrolled in education.",
        "benefit_summary": "₹1,000/yr school scholarship (K1) + ₹25,000 one-time grant on attaining age 18 (K2)",
        "benefit_type": "Scholarship / Educational Aid",
        "max_financial_benefit": "₹25,000 One-time Grant + ₹1,000/year",
        "eligibility_criteria": [
            "Unmarried girl student resident of West Bengal",
            "K1: Age 13-18 years studying in Class 8 to 12 in recognized institution",
            "K2: Girl student turning 18 years, enrolled in higher education, and unmarried"
        ],
        "target_beneficiaries": ["Girl Students in West Bengal"],
        "eligibility_rules": {
            "min_age": 13,
            "max_age": 19,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["Student"],
            "state_restriction": ["West Bengal"],
            "marital_status": ["single"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "School / College Bonafide Certificate", "mandatory": True, "description": "Proof of current year enrollment", "how_to_get": "Headmaster/Principal"},
            {"name": "Birth Certificate", "mandatory": True, "description": "Proof of age", "how_to_get": "Panchayat / Municipality"},
            {"name": "Unmarried Status Declaration", "mandatory": True, "description": "Self and parent declaration", "how_to_get": "School form"},
            {"name": "Bank Passbook in Girl's Name", "mandatory": True, "description": "Individual account for DBT", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Collect Form from School / College", "description": "Kanyashree forms are distributed directly by the school/college authority."},
            {"step_number": 2, "title": "Fill Details & Submit to Head of Institution", "description": "Attach birth certificate, bank passbook copy, and unmarried declaration."},
            {"step_number": 3, "title": "Online Upload by School", "description": "School Nodal Officer uploads to https://wbkanyashree.gov.in; funds disbursed directly by state treasury."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://wbkanyashree.gov.in",
        "india_gov_url": "https://www.india.gov.in/kanyashree-prakalpa-scheme-west-bengal",
        "helpline": "033-23373840 / 1098",
        "faq": [
            {"question": "Is there any family income ceiling for Kanyashree?", "answer": "The income ceiling has been removed by Govt of WB; all unmarried girl students enrolled in education are eligible."}
        ],
        "tags": ["west bengal", "girls", "scholarship", "anti child marriage", "state scheme"],
        "featured": True
    },
    {
        "id": "kanya-sumangala-up",
        "title": "Mukhyamantri Kanya Sumangala Yojana (Uttar Pradesh)",
        "title_hi": "मुख्यमंत्री कन्या सुमंगला योजना (उत्तर प्रदेश)",
        "short_name": "UP Kanya Sumangala",
        "ministry": "Department of Women & Child Development, Govt of Uttar Pradesh",
        "sector": "Women & Child",
        "is_central": False,
        "applicable_states": ["Uttar Pradesh"],
        "description": "Financial assistance program by the Government of Uttar Pradesh providing a total of ₹25,000 cash grant in six installments from the birth of a girl child through her complete vaccination, school admission (Class 1, 6, 9), and graduation degree/diploma enrollment.",
        "benefit_summary": "₹25,000 cash assistance released in 6 developmental phases from birth to graduation",
        "benefit_type": "Scholarship / Educational Aid",
        "max_financial_benefit": "₹25,000 Phased Grant",
        "eligibility_criteria": [
            "Permanent resident of Uttar Pradesh with valid Domicile",
            "Family annual income not exceeding ₹3,00,000",
            "Maximum 2 girl children per family eligible (3 in case of twin girls in second delivery)"
        ],
        "target_beneficiaries": ["Girl Children & Parents in Uttar Pradesh"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 25,
            "genders": ["female"],
            "categories": ["All"],
            "occupations": ["All"],
            "max_annual_income": 300000,
            "state_restriction": ["Uttar Pradesh"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "UP Domicile / Residence Certificate", "mandatory": True, "description": "Proof of residence in UP", "how_to_get": "eDistrict UP portal"},
            {"name": "Birth Certificate of Girl Child", "mandatory": True, "description": "Proof of age and parentage", "how_to_get": "Municipality / Panchayat"},
            {"name": "Income Certificate (below ₹3 Lakhs)", "mandatory": True, "description": "Issued by Tehsildar", "how_to_get": "eDistrict UP"},
            {"name": "School Admission / Vaccination Card", "mandatory": True, "description": "Required according to installment stage", "how_to_get": "School / Hospital"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on MKSY Portal", "description": "Visit https://mksy.up.gov.in and create Citizen Service account."},
            {"step_number": 2, "title": "Select Applicable Stage (1 to 6)", "description": "Stage 1 (Birth: ₹5k), Stage 2 (Vaccination: ₹2k), Stage 3 (Class 1: ₹3k), Stage 4 (Class 6: ₹3k), Stage 5 (Class 9: ₹5k), Stage 6 (Graduation: ₹7k)."},
            {"step_number": 3, "title": "Upload Certificates & Verification", "description": "SDM / BDO approves application; amount credited directly to parent/girl bank account."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://mksy.up.gov.in",
        "india_gov_url": "https://www.india.gov.in/mukhyamantri-kanya-sumangala-yojana-uttar-pradesh",
        "helpline": "181 / 0522-2287234",
        "faq": [
            {"question": "When was the grant increased to ₹25,000?", "answer": "Govt of UP enhanced the total benefit package from ₹15,000 to ₹25,000 starting financial year 2024-25."}
        ],
        "tags": ["uttar pradesh", "girls", "education", "maternity", "state scheme"],
        "featured": True
    },
    {
        "id": "rythu-bandhu-telangana",
        "title": "Rythu Bandhu / Rythu Bharosa (Telangana / Andhra Pradesh)",
        "title_hi": "रायथु बंधु / रायथु भरोसा (तेलंगाना / आंध्र प्रदेश)",
        "short_name": "Rythu Bandhu Farmer Aid",
        "ministry": "Agriculture & Farmers Welfare Department",
        "sector": "Agriculture",
        "is_central": False,
        "applicable_states": ["Telangana", "Andhra Pradesh"],
        "description": "Direct investment support scheme for agriculture and horticulture crops, transferring ₹10,000 to ₹13,500 per acre per year directly into farmers' bank accounts across Kharif and Rabi seasons to purchase quality seeds, fertilizers, and farm inputs.",
        "benefit_summary": "₹10,000 to ₹13,500 per acre per year direct input subsidy (₹5,000 - ₹7,500/season)",
        "benefit_type": "Direct Benefit Transfer (Cash)",
        "max_financial_benefit": "₹10,000 - ₹13,500 / acre / year",
        "eligibility_criteria": [
            "Landowner farmers possessing Pattadar Passbook / Dharani land records",
            "Resident of Telangana or Andhra Pradesh cultivating agricultural land",
            "Applicable for both Kharif and Rabi cropping seasons"
        ],
        "target_beneficiaries": ["Farmers in Telangana & Andhra Pradesh", "Landholders"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 85,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Farmer / Agriculture", "Fisherfolk / Dairy Farmer"],
            "requires_land": True,
            "state_restriction": ["Telangana", "Andhra Pradesh"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Pattadar Passbook (Dharani Portal / Meebhoomi)", "mandatory": True, "description": "Title deed proof of agricultural land", "how_to_get": "Dharani portal / MeeSeva"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity verification", "how_to_get": "UIDAI"},
            {"name": "Bank Passbook with Aadhaar Linking", "mandatory": True, "description": "Account for direct investment disbursement", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Automatic Listing from Dharani Land Records", "description": "Eligible farmers are auto-mapped from Dharani / Webland digital title deeds."},
            {"step_number": 2, "title": "Verification by Agriculture Extension Officer (AEO)", "description": "AEO verifies active bank account and Aadhaar linkage."},
            {"step_number": 3, "title": "Direct Treasury Credit", "description": "Amount credited per acre at the beginning of each crop season."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://rythubandhu.telangana.gov.in",
        "india_gov_url": "https://www.india.gov.in/rythu-bandhu-scheme-farmers-investment-support-scheme",
        "helpline": "040-23383520",
        "faq": [
            {"question": "Is there any ceiling on land acreage?", "answer": "The assistance is paid based on registered cultivable acreage directly to all Pattadar landholders."}
        ],
        "tags": ["telangana", "andhra pradesh", "farmer", "dbt", "input subsidy", "state scheme"],
        "featured": True
    },
    {
        "id": "pm-kusum-solar-pump",
        "title": "Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyan (PM-KUSUM)",
        "title_hi": "प्रधानमंत्री किसान ऊर्जा सुरक्षा एवं उत्थान महाभियान (पीएम-कुसुम)",
        "short_name": "PM-KUSUM Solar Pump",
        "ministry": "Ministry of New and Renewable Energy",
        "sector": "Agriculture",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Provides up to 60% government subsidy to farmers for installing standalone solar agricultural water pumps (up to 7.5 HP) or solarizing existing diesel/electric pumps, with another 30% bank loan support so farmer pays only 10% upfront.",
        "benefit_summary": "60% Subsidy on standalone solar agriculture pumps (3HP to 7.5HP) + 30% bank loan",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "60% Government Subsidy (up to ₹2,50,000)",
        "eligibility_criteria": [
            "Individual farmers, groups of farmers, Water User Associations, and Cooperatives",
            "Must possess agricultural land and need for irrigation pumping",
            "Must have valid Aadhaar and bank details"
        ],
        "target_beneficiaries": ["Farmers", "Agricultural Landholders", "Water User Groups"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Farmer / Agriculture"],
            "requires_land": True,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Land Record (7-12 / Khatauni / RoR)", "mandatory": True, "description": "Proof of agricultural land and water source", "how_to_get": "Revenue Patwari"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity proof", "how_to_get": "UIDAI"},
            {"name": "Bank Passbook", "mandatory": True, "description": "For subsidy and loan sanction", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply on State Solar Portal", "description": "Visit State Renewable Energy Development Agency portal linked from https://pmkusum.mnre.gov.in."},
            {"step_number": 2, "title": "Select Pump Capacity (3HP / 5HP / 7.5HP)", "description": "Choose DC/AC submersible solar pump."},
            {"step_number": 3, "title": "Pay 10% Farmer Share & Installation", "description": "Empaneled solar vendor installs pump and commissions within 90 days."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://pmkusum.mnre.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pm-kusum-scheme",
        "helpline": "1800-180-3333",
        "faq": [
            {"question": "Can I sell excess solar power?", "answer": "Under Component C, grid-connected solar pumps can export excess electricity back to DISCOM for additional income."}
        ],
        "tags": ["solar pump", "farmer", "agriculture", "energy", "subsidy", "central"],
        "featured": False
    },
    {
        "id": "pm-krishi-sinchayee-pdmc",
        "title": "PM Krishi Sinchayee Yojana (Per Drop More Crop)",
        "title_hi": "प्रधानमंत्री कृषि सिंचाई योजना (पर ड्रॉप मोर क्रॉप)",
        "short_name": "PMKSY Micro Irrigation",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "sector": "Agriculture",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Offers 55% financial assistance for small/marginal farmers and 45% for other farmers to install precision micro-irrigation technologies (Drip and Sprinkler irrigation systems) to maximize water efficiency, reduce fertilizer expenditure, and boost crop productivity by 40%.",
        "benefit_summary": "55% Subsidy for small/marginal farmers on Drip and Sprinkler micro-irrigation systems",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "55% Capital Subsidy on Micro Irrigation",
        "eligibility_criteria": [
            "All categories of farmers owning or leasing cultivable land with an assured water source",
            "Special preference to small and marginal farmers, SC/ST, and women farmers"
        ],
        "target_beneficiaries": ["Small & Marginal Farmers", "Horticulture Growers", "All Farmers"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 80,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Farmer / Agriculture"],
            "requires_land": True,
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Land Record (7/12, Khatauni)", "mandatory": True, "description": "Proof of landholding", "how_to_get": "Revenue Patwari"},
            {"name": "Water Source Certificate", "mandatory": True, "description": "Proof of open well/borewell/canal connectivity", "how_to_get": "Village Officer"},
            {"name": "Aadhaar & Bank Passbook", "mandatory": True, "description": "KYC and DBT account", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply at District Horticulture/Agriculture Office", "description": "Submit application online on state micro-irrigation portal."},
            {"step_number": 2, "title": "Field Survey & Design Estimation", "description": "Horticulture officer and vendor inspect plot layout and water discharge."},
            {"step_number": 3, "title": "Installation & DBT Subsidy", "description": "Direct subsidy credited to farmer/vendor account after verification."}
        ],
        "application_mode": "Hybrid",
        "official_portal_url": "https://pmksy.gov.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/pradhan-mantri-krishi-sinchayee-yojana",
        "helpline": "011-23383370",
        "faq": [
            {"question": "What is the water saving through drip irrigation?", "answer": "Drip irrigation saves up to 40-70% water and increases crop yield by up to 30-50%."}
        ],
        "tags": ["drip irrigation", "farmer", "agriculture", "subsidy", "central"],
        "featured": False
    },
    {
        "id": "cgtmse-msme-credit",
        "title": "Credit Guarantee Scheme for Micro & Small Enterprises (CGTMSE)",
        "title_hi": "सूक्ष्म एवं लघु उद्यमों के लिए क्रेडिट गारंटी योजना (सीजीटीएमएसई)",
        "short_name": "CGTMSE Collateral-Free Credit",
        "ministry": "Ministry of Micro, Small and Medium Enterprises",
        "sector": "Employment & MSME",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Enables new and existing Micro and Small Enterprises to secure collateral-free institutional credit (term loans and working capital) up to ₹5 Crore from commercial banks and NBFCs with up to 85% government-backed credit guarantee cover.",
        "benefit_summary": "Collateral-free bank loans up to ₹5 Crore with 75%-85% credit guarantee coverage",
        "benefit_type": "Subsidized Loan",
        "max_financial_benefit": "Up to ₹5 Crore Collateral-Free Bank Credit",
        "eligibility_criteria": [
            "New and existing Micro and Small Enterprises (MSEs) engaged in manufacturing or service activities",
            "Retail trade credit up to ₹2 Crore also eligible",
            "Educational institutions and training institutes recognized as MSEs"
        ],
        "target_beneficiaries": ["MSME Entrepreneurs", "Small Manufacturers", "Tech Startups", "Women Enterprises"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 65,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Self-Employed / Micro Business", "Salaried (Private/Public)"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Udyam Registration Certificate", "mandatory": True, "description": "Proof of MSME registration", "how_to_get": "udyamregistration.gov.in"},
            {"name": "Detailed Project Report (DPR) & Financials", "mandatory": True, "description": "Cash flow projections, balance sheet, and ITR", "how_to_get": "Chartered Accountant"},
            {"name": "PAN & Aadhaar of Promoters", "mandatory": True, "description": "KYC verification", "how_to_get": "UIDAI / IT Dept"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Submit Loan Application to Member Lending Bank", "description": "Approach any scheduled commercial bank or apply via JanSamarth portal."},
            {"step_number": 2, "title": "Request CGTMSE Coverage", "description": "Inform bank to process under CGTMSE guarantee without third-party collateral."},
            {"step_number": 3, "title": "Loan Sanction & Guarantee Issuance", "description": "Bank sanctions loan and obtains guarantee cover from CGTMSE trust directly."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.cgtmse.in",
        "india_gov_url": "https://www.india.gov.in/credit-guarantee-fund-scheme-micro-and-small-enterprises",
        "helpline": "022-67531100 / 022-67221553",
        "faq": [
            {"question": "What is the guarantee cover for women entrepreneurs?", "answer": "Women entrepreneurs and micro-enterprises receive higher guarantee cover of up to 85%."}
        ],
        "tags": ["cgtmse", "collateral free loan", "msme", "credit guarantee", "central"],
        "featured": False
    },
    {
        "id": "national-apprenticeship-naps",
        "title": "National Apprenticeship Promotion Scheme (NAPS-2)",
        "title_hi": "राष्ट्रीय शिक्षुता संवर्धन योजना (एनएपीएस-2)",
        "short_name": "NAPS Apprenticeship",
        "ministry": "Ministry of Skill Development and Entrepreneurship",
        "sector": "Education & Skills",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Promotes apprenticeship training across Indian industries by providing monthly stipend support of 25% (up to ₹1,500/month) directly into candidate's bank account via DBT during 6 to 36 months of practical corporate on-job training.",
        "benefit_summary": "Monthly stipend (₹7,000 - ₹15,000/mo) with direct government DBT top-up + National Apprenticeship Certificate",
        "benefit_type": "Scholarship / Educational Aid",
        "max_financial_benefit": "Monthly Stipend + ₹1,500/mo DBT Support",
        "eligibility_criteria": [
            "Indian candidates aged 14 years and above (18+ for hazardous industries)",
            "Holding minimum 5th, 8th, 10th, 12th pass, ITI certificate, Diploma, or Graduate degree",
            "Registered on Apprenticeship India portal"
        ],
        "target_beneficiaries": ["ITI Passouts", "Diploma Holders", "Graduates", "Skill Seekers"],
        "eligibility_rules": {
            "min_age": 14,
            "max_age": 35,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["Student", "Unemployed / Jobseeker"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Educational Marksheet (10th/12th/ITI/Degree)", "mandatory": True, "description": "Proof of educational qualification", "how_to_get": "Board/University"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Candidate identity and eKYC", "how_to_get": "UIDAI"},
            {"name": "Aadhaar-Linked Bank Account", "mandatory": True, "description": "For direct government stipend share credit", "how_to_get": "Bank branch"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Register on Apprenticeship India Portal", "description": "Visit https://www.apprenticeshipindia.gov.in and complete 100% profile."},
            {"step_number": 2, "title": "Search & Apply for Apprenticeship Opportunities", "description": "Filter by industry (Automotive, IT, Manufacturing, Banking) and location."},
            {"step_number": 3, "title": "Sign Digital Apprenticeship Contract", "description": "Employer issues contract; undergo practical industry training with monthly stipend."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://www.apprenticeshipindia.gov.in",
        "india_gov_url": "https://www.india.gov.in/national-apprenticeship-promotion-scheme",
        "helpline": "011-23450850",
        "faq": [
            {"question": "Do I get a certificate after completion?", "answer": "Yes, on clearing the All India Trade Test (AITT), you receive the National Apprenticeship Certificate (NAC) recognized across India."}
        ],
        "tags": ["apprenticeship", "stipend", "on the job training", "skill india", "central"],
        "featured": False
    },
    {
        "id": "poshan-abhiyaan-nutrition",
        "title": "Poshan Abhiyaan (National Nutrition Mission)",
        "title_hi": "पोषण अभियान (राष्ट्रीय पोषण मिशन)",
        "short_name": "Poshan Abhiyaan Nutrition",
        "ministry": "Ministry of Women and Child Development",
        "sector": "Women & Child",
        "is_central": True,
        "applicable_states": ["All"],
        "description": "Comprehensive mission to reduce stunting, under-nutrition, anemia among young children (0-6 years), adolescent girls, pregnant women, and lactating mothers through Take-Home Rations (THR), hot cooked meals, growth monitoring on Poshan Tracker app, and micronutrient supplementation.",
        "benefit_summary": "Free monthly nutritious rations, supplementary nutrition, growth monitoring, and health tracking at Anganwadi",
        "benefit_type": "Asset / Equipment Subsidy",
        "max_financial_benefit": "Free Monthly Nutrition Food Kits & Health Monitoring",
        "eligibility_criteria": [
            "Children from 6 months to 6 years of age",
            "Pregnant women and lactating mothers",
            "Adolescent girls (14-18 years) in aspirational districts"
        ],
        "target_beneficiaries": ["Children (0-6 yrs)", "Pregnant Women", "Lactating Mothers", "Adolescent Girls"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 45,
            "genders": ["female", "any"],
            "categories": ["All"],
            "occupations": ["All"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "Aadhaar Card of Mother / Child", "mandatory": True, "description": "Registration on Poshan Tracker", "how_to_get": "UIDAI"},
            {"name": "MCP Card", "mandatory": True, "description": "Vaccination and health records", "how_to_get": "Anganwadi"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Visit Local Anganwadi Centre", "description": "Meet Anganwadi worker and register child/mother profile."},
            {"step_number": 2, "title": "Collect Monthly Take-Home Ration (THR)", "description": "Receive nutrient-rich fortified food kits (Dalia, pulses, fortified oil, millets)."},
            {"step_number": 3, "title": "Monthly Growth Monitoring", "description": "Height/weight plotted on Poshan Tracker app to ensure healthy developmental milestones."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://www.poshantracker.in",
        "india_gov_url": "https://www.india.gov.in/spotlight/poshan-abhiyaan",
        "helpline": "14408 / 1098",
        "faq": [
            {"question": "Is Poshan Abhiyaan free of cost?", "answer": "Yes, all supplementary nutrition and health monitoring services at Anganwadi centers are 100% free."}
        ],
        "tags": ["poshan", "nutrition", "children", "mothers", "anganwadi", "central"],
        "featured": False
    },
    {
        "id": "biju-swasthya-kalyan-odisha",
        "title": "Biju Swasthya Kalyan Yojana (BSKY - Odisha)",
        "title_hi": "बीजू स्वास्थ्य कल्याण योजना (ओडिशा)",
        "short_name": "Odisha BSKY Health Card",
        "ministry": "Health & Family Welfare Department, Govt of Odisha",
        "sector": "Healthcare",
        "is_central": False,
        "applicable_states": ["Odisha"],
        "description": "Universal health protection scheme in Odisha providing cashless treatment of up to ₹5,00,000 per family per year, and enhanced coverage of up to ₹10,00,000 for female family members across all government and 800+ empaneled private hospitals.",
        "benefit_summary": "₹5 Lakhs/family + ₹10 Lakhs for female members cashless hospital treatment at empaneled hospitals",
        "benefit_type": "Health Coverage",
        "max_financial_benefit": "₹5 Lakhs - ₹10 Lakhs Cashless Health Cover",
        "eligibility_criteria": [
            "All BPL / Antyodaya / Ration cardholder families resident of Odisha",
            "BSKY Nabin Card holders covering rural households",
            "Free healthcare at all government health facilities from Sub-Centre to Medical Colleges for all residents"
        ],
        "target_beneficiaries": ["Resident Families in Odisha", "Women in Odisha", "Low-Income Households"],
        "eligibility_rules": {
            "min_age": 0,
            "max_age": 100,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "state_restriction": ["Odisha"],
            "area_type": "any"
        },
        "required_documents": [
            {"name": "BSKY Smart Health Card / Ration Card", "mandatory": True, "description": "Proof of Odisha NFSA/SFSS beneficiary status", "how_to_get": "Food & Civil Supplies Odisha"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Patient biometric authentication at hospital helpdesk", "how_to_get": "UIDAI"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Check BSKY Card Activation", "description": "Verify your family card at https://bsky.odisha.gov.in."},
            {"step_number": 2, "title": "Visit BSKY Empaneled Hospital", "description": "Approach BSKY Swasthya Mitra desk at hospital admission."},
            {"step_number": 3, "title": "Biometric Authentication & Treatment", "description": "100% cashless treatment, tests, surgery, and post-discharge medicines."}
        ],
        "application_mode": "Offline / CSC / Gram Panchayat",
        "official_portal_url": "https://bsky.odisha.gov.in",
        "india_gov_url": "https://www.india.gov.in/biju-swasthya-kalyan-yojana-odisha",
        "helpline": "104 / 155369",
        "faq": [
            {"question": "What is the enhanced benefit for women?", "answer": "Women family members are entitled to up to ₹10,00,000 in secondary and tertiary treatment expenses."}
        ],
        "tags": ["odisha", "bsky", "health insurance", "cashless", "women health", "state scheme"],
        "featured": True
    },
    {
        "id": "mo-ghara-odisha",
        "title": "Mo Ghara (My House) Credit-Linked Housing Scheme (Odisha)",
        "title_hi": "मो घरा (मेरा घर) आवास योजना (ओडिशा)",
        "short_name": "Odisha Mo Ghara",
        "ministry": "Panchayati Raj & Drinking Water Department, Govt of Odisha",
        "sector": "Housing & Sanitation",
        "is_central": False,
        "applicable_states": ["Odisha"],
        "description": "Credit-linked housing scheme by Govt of Odisha offering capital subsidy up to ₹60,000 to ₹70,000 on bank housing loans up to ₹3,00,000 for rural households to convert kutcha houses or upgrade their existing houses.",
        "benefit_summary": "Up to ₹70,000 government subsidy on housing loan of ₹3,00,000 (10-year flexible tenure)",
        "benefit_type": "Housing Grant",
        "max_financial_benefit": "Up to ₹70,000 Government Subsidy",
        "eligibility_criteria": [
            "Rural family in Odisha living in a kutcha house or having 1 pucca room with RCC roof",
            "Monthly family income below ₹25,000 and not having 4-wheeler or government employee in family",
            "Has not received previous housing assistance of ₹70k+ under PMAY/BAP"
        ],
        "target_beneficiaries": ["Rural Families in Odisha", "Kutcha House Residents", "Lower Middle Class"],
        "eligibility_rules": {
            "min_age": 18,
            "max_age": 70,
            "genders": ["any"],
            "categories": ["All"],
            "occupations": ["All"],
            "state_restriction": ["Odisha"],
            "area_type": "rural"
        },
        "required_documents": [
            {"name": "Land RoR / Patta in Rural Odisha", "mandatory": True, "description": "Proof of residential homestead land", "how_to_get": "Bhulekh Odisha"},
            {"name": "Aadhaar Card", "mandatory": True, "description": "Identity verification", "how_to_get": "UIDAI"},
            {"name": "Income Certificate / Self-Declaration", "mandatory": True, "description": "Monthly income below ₹25,000", "how_to_get": "Tehsildar"}
        ],
        "application_steps": [
            {"step_number": 1, "title": "Apply on Mo Ghara Portal", "description": "Visit https://moghara.odisha.gov.in and choose loan slab (₹1L, ₹1.5L, ₹2L, ₹3L)."},
            {"step_number": 2, "title": "BDO Field Verification", "description": "Block Development Officer geo-tags house and verifies criteria."},
            {"step_number": 3, "title": "Bank Loan Sanction & Subsidy Credit", "description": "Bank disburses loan; state subsidy credited on house completion."}
        ],
        "application_mode": "Online Portal",
        "official_portal_url": "https://moghara.odisha.gov.in",
        "india_gov_url": "https://www.india.gov.in/mo-ghara-scheme-odisha",
        "helpline": "155335 / 0674-2536780",
        "faq": [
            {"question": "Can SC/ST and PwD beneficiaries get higher subsidy?", "answer": "Yes, SC, ST, and PwD headed households receive maximum subsidy of ₹70,000."}
        ],
        "tags": ["odisha", "housing", "subsidy", "rural", "state scheme"],
        "featured": False
    }

]

# ---------------------------------------------------------------------------
# Real application cut-off dates, keyed by scheme id. Kept separate from the
# scheme bodies so the dates can be reviewed in one place.
# window_type: ROLLING (open all year) | ANNUAL | SEASONAL | EVENT_BASED
# Dates are recurring annual (month, day) — the API computes the next occurrence
# against the IST server clock.
# ---------------------------------------------------------------------------
SCHEME_DEADLINES = {
    "pm-fasal-bima": {
        "window_type": "SEASONAL",
        "cutoff_dates": [
            {"label": "Kharif season enrolment", "month": 7, "day": 31},
            {"label": "Rabi season enrolment", "month": 12, "day": 31},
        ],
        "source_note": "State governments may notify crop-specific dates slightly earlier.",
    },
    "post-matric-scholarship-sc-st-obc": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "National Scholarship Portal (NSP) application", "month": 10, "day": 31}],
        "source_note": "Institute verification usually closes ~15 days after the student deadline.",
    },
    "pragati-scholarship-girls": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "AICTE Pragati application on NSP", "month": 10, "day": 31}],
    },
    "pm-kisan": {
        "window_type": "SEASONAL",
        "cutoff_dates": [
            {"label": "Instalment 1 (Apr-Jul) eKYC", "month": 5, "day": 31},
            {"label": "Instalment 2 (Aug-Nov) eKYC", "month": 9, "day": 30},
            {"label": "Instalment 3 (Dec-Mar) eKYC", "month": 1, "day": 31},
        ],
        "source_note": "Registration is open year-round, but eKYC must be done before each instalment cycle.",
    },
    "pm-surya-ghar-muft-bijli": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "Financial-year subsidy allocation", "month": 3, "day": 31}],
        "source_note": "Subsidy is released against the FY budget — applying early avoids queueing.",
    },
    "pm-kusum-solar-pump": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "State solar pump allocation round", "month": 3, "day": 31}],
        "source_note": "State agencies open limited quota rounds each financial year.",
    },
    "pm-krishi-sinchayee-pdmc": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "Micro-irrigation subsidy allocation", "month": 3, "day": 31}],
    },
    "kanyashree-prakalpa-wb": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "K1/K2 annual renewal through institution", "month": 10, "day": 15}],
    },
    "yuva-nidhi-karnataka": {
        "window_type": "EVENT_BASED",
        "note": "Apply after completing 180 days (6 months) of unemployment from your result date. A monthly self-declaration is required to keep the stipend running.",
    },
    "pm-matru-vandana": {
        "window_type": "EVENT_BASED",
        "note": "Register within 270 days of your Last Menstrual Period (LMP) date. The second instalment must be claimed after birth registration and the first vaccination cycle.",
    },
    "sukanya-samriddhi-yojana": {
        "window_type": "EVENT_BASED",
        "note": "The account must be opened before the girl child turns 10 years old — the window closes permanently on her 10th birthday.",
    },
    "kanya-sumangala-up": {
        "window_type": "EVENT_BASED",
        "note": "Each of the 6 stages must be claimed within its own event window (birth, vaccination, Class 1, Class 6, Class 9, graduation).",
    },
    "national-apprenticeship-naps": {
        "window_type": "EVENT_BASED",
        "note": "Employers post apprenticeship vacancies with their own closing dates — check the portal monthly for new batches.",
    },
    "adip-disability-aids": {
        "window_type": "EVENT_BASED",
        "note": "Distribution happens through district ALIMCO assessment camps. Register with your DDRC to be called for the next camp in your district.",
    },
    "rashtriya-vayoshri-yojana": {
        "window_type": "EVENT_BASED",
        "note": "Aids are distributed at district-level camps organised by the Social Welfare Officer — enrol to be notified of the next camp.",
    },
    "pm-jeevan-jyoti-bima": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "Annual policy renewal (cover runs 1 Jun - 31 May)", "month": 5, "day": 31}],
    },
    "pm-suraksha-bima": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "Annual policy renewal (cover runs 1 Jun - 31 May)", "month": 5, "day": 31}],
    },
    "rythu-bandhu-telangana": {
        "window_type": "SEASONAL",
        "cutoff_dates": [
            {"label": "Kharif investment support cycle", "month": 6, "day": 30},
            {"label": "Rabi investment support cycle", "month": 12, "day": 31},
        ],
    },
    "pm-egp-subsidy": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "Financial-year margin money allocation", "month": 3, "day": 31}],
        "source_note": "KVIC processes applications against the annual FY target.",
    },
    "mo-ghara-odisha": {
        "window_type": "ANNUAL",
        "cutoff_dates": [{"label": "Financial-year housing loan sanction target", "month": 3, "day": 31}],
    },
}

ROLLING_DEADLINE_NOTES = {
    "ayushman-bharat-pmjay": "Ayushman card eKYC is open all year — you can generate your card any day and use it immediately at an empanelled hospital.",
    "pm-awas-gramin": "Applications flow continuously through Awaas+ surveys and Gram Sabha approval — there is no annual cut-off, but the Gram Sabha list is finalised at each meeting.",
    "pm-vishwakarma": "Artisan registration at CSC centres is open all year, subject to the scheme's overall five-year mission period.",
    "pm-svanidhi": "Working-capital loan applications are accepted throughout the year at any lending branch.",
    "pm-mudra-yojana": "Mudra loan applications are accepted by banks all year with no seasonal window.",
    "mgnrega-employment": "Work can be demanded on any day of the year — the Panchayat must allot work within 15 days of your written demand.",
    "atal-pension-yojana": "Enrolment is open all year until you turn 40 — joining earlier means a lower monthly contribution.",
    "ignoaps-old-age-pension": "Pension applications are accepted throughout the year at the Block or Municipality office.",
    "kisan-credit-card": "KCC applications are accepted year-round; banks must decide within 14 days.",
    "pm-ujjwala-yojana": "Free LPG connections are issued all year at any Indane, Bharatgas or HP Gas distributor.",
    "pmkvy-skills": "New training batches start continuously — enrol any time and join the next batch at your Kaushal Kendra.",
    "pm-janaushadhi": "No application needed — simply walk into any Jan Aushadhi Kendra with a prescription on any day.",
    "stand-up-india": "Loan applications are accepted year-round through the Stand-Up Mitra portal.",
    "cgtmse-msme-credit": "Guarantee cover is issued whenever the bank sanctions your loan — no seasonal window.",
    "mahila-samman-savings": "Deposits can be made any day, subject to the scheme's overall availability period notified by the Ministry of Finance.",
    "lakhpati-didi": "Enrolment happens continuously through your village SHG and Cluster Level Federation.",
    "poshan-abhiyaan-nutrition": "Register at your Anganwadi on any day — monthly take-home rations begin immediately.",
    "ladli-behna-mp": "Applications are accepted in rolling Gram Panchayat and ward camps notified by the state.",
    "gruha-lakshmi-karnataka": "Enrolment is open all year at Grama One, Karnataka One and Bangalore One centres.",
    "biju-swasthya-kalyan-odisha": "No application window — present your BSKY or ration card at an empanelled hospital whenever treatment is needed.",
}

MASTER_DOCUMENTS_DATA = [
    {
        "id": "aadhaar",
        "name": "Aadhaar Card",
        "name_hi": "आधार कार्ड",
        "category": "Identity",
        "description": "12-digit unique biometric identification issued by UIDAI, mandatory for eKYC and Direct Benefit Transfer (DBT).",
        "issuing_authority": "Unique Identification Authority of India (UIDAI)",
        "how_to_obtain": "Enroll at nearest Aadhaar Seva Kendra or update online at myaadhaar.uidai.gov.in.",
        "digital_portal_url": "https://myaadhaar.uidai.gov.in",
        "common_schemes_count": 42,
        "common_schemes": ["PM-KISAN", "Ayushman Bharat", "PMAY", "PM Vishwakarma", "PM Mudra", "PM SVANidhi"]
    },
    {
        "id": "bank_passbook",
        "name": "Aadhaar-Linked Bank Passbook (NPCI Seeded)",
        "name_hi": "आधार लिंक बैंक पासबुक (एनपीसीआई मैप्ड)",
        "category": "Income & Financial",
        "description": "Active savings bank account seeded with Aadhaar on NPCI mapper for receiving government cash subsidies.",
        "issuing_authority": "Any Nationalized / Commercial / Grameen Bank or Post Office",
        "how_to_obtain": "Visit your bank branch with Aadhaar copy and submit 'Aadhaar Seeding / DBT Consent Form'.",
        "digital_portal_url": "https://www.npci.org.in",
        "common_schemes_count": 38,
        "common_schemes": ["PM-KISAN", "PM SVANidhi", "MGNREGA", "Post-Matric Scholarship", "PMMVY", "Ladli Behna"]
    },
    {
        "id": "ration_card",
        "name": "Ration Card (BPL / Antyodaya / Priority NFSA)",
        "name_hi": "राशन कार्ड (बीपीएल / अंत्योदय)",
        "category": "Income & Financial",
        "description": "Official family document certifying household economic category and subsidized food grain entitlement.",
        "issuing_authority": "Department of Food, Civil Supplies & Consumer Affairs (State Gov)",
        "how_to_obtain": "Apply through State Food Portal or nearest CSC / Gram Panchayat office.",
        "digital_portal_url": "https://nfsa.gov.in",
        "common_schemes_count": 28,
        "common_schemes": ["Ayushman Bharat", "PMAY-G", "PM Ujjwala", "Rashtriya Vayoshri", "IGNOAPS"]
    },
    {
        "id": "income_certificate",
        "name": "Annual Family Income Certificate",
        "name_hi": "आय प्रमाण पत्र",
        "category": "Income & Financial",
        "description": "Official revenue certificate stating total annual household income from all sources for quota/subsidy eligibility.",
        "issuing_authority": "Tehsildar / Sub-Divisional Magistrate (SDM) / Revenue Dept",
        "how_to_obtain": "Apply via State e-District portal or Tehsildar office with salary slip / self-declaration.",
        "digital_portal_url": "https://edistrict.gov.in",
        "common_schemes_count": 25,
        "common_schemes": ["Post-Matric Scholarship", "Pragati Scholarship", "PMEGP", "Kanya Sumangala"]
    },
    {
        "id": "caste_certificate",
        "name": "Caste / Category Certificate (SC / ST / OBC / EWS)",
        "name_hi": "जाति प्रमाण पत्र (एससी / एसटी / ओबीसी / ईडब्ल्यूएस)",
        "category": "Social & Caste",
        "description": "Legal document confirming applicant's social category for affirmative action and targeted welfare reservations.",
        "issuing_authority": "District Magistrate / Sub-Divisional Officer (SDO) / Tehsildar",
        "how_to_obtain": "Apply online at State e-District portal or CSC center with ancestral proof.",
        "digital_portal_url": "https://edistrict.gov.in",
        "common_schemes_count": 20,
        "common_schemes": ["Post-Matric Scholarship", "Stand-Up India", "PMEGP", "PM Vishwakarma"]
    },
    {
        "id": "domicile_certificate",
        "name": "Domicile / Permanent Residence Certificate",
        "name_hi": "मूल निवास / अधिवास प्रमाण पत्र",
        "category": "Residence & Land",
        "description": "Proof of permanent residency in a particular State or Union Territory.",
        "issuing_authority": "District Administration / Revenue Authority",
        "how_to_obtain": "Apply on State e-District portal with electricity bill, voter ID, and school leaving certificate.",
        "digital_portal_url": "https://edistrict.gov.in",
        "common_schemes_count": 18,
        "common_schemes": ["Ladli Behna", "Gruha Lakshmi", "Yuva Nidhi", "Kanyashree", "Kanya Sumangala"]
    },
    {
        "id": "land_record",
        "name": "Agricultural Land Record (Khatauni / 7-12 / RoR / Patta)",
        "name_hi": "भू-अभिलेख / खतौनी / 7/12 नकल",
        "category": "Residence & Land",
        "description": "Certified digital land record extract proving ownership and survey numbers of agricultural land.",
        "issuing_authority": "State Bhulekh / Land Revenue Department",
        "how_to_obtain": "Download digitally signed RoR from State Bhulekh portal (e.g. upbhulekh.gov.in, mahabhumi, dharani).",
        "digital_portal_url": "https://bhulekh.gov.in",
        "common_schemes_count": 12,
        "common_schemes": ["PM-KISAN", "PM Fasal Bima", "Kisan Credit Card", "Rythu Bandhu", "PMKSY"]
    },
    {
        "id": "udid_card",
        "name": "Disability Certificate / UDID Card",
        "name_hi": "दिव्यांगता प्रमाण पत्र / यूडीआईडी कार्ड",
        "category": "Special Category",
        "description": "Unique Disability ID card issued by medical board showing percentage of benchmark disability (40%+).",
        "issuing_authority": "Department of Empowerment of Persons with Disabilities (DEPwD)",
        "how_to_obtain": "Apply on Swavlamban portal (swavlambancard.gov.in) and attend assessment at District Hospital.",
        "digital_portal_url": "https://www.swavlambancard.gov.in",
        "common_schemes_count": 10,
        "common_schemes": ["ADIP Assistive Aids", "Divyangjan Pension", "Accessible India Schemes"]
    },
    {
        "id": "mgnrega_card",
        "name": "MGNREGA Job Card",
        "name_hi": "मनरेगा जॉब कार्ड",
        "category": "Education & Employment",
        "description": "Official employment card issued to rural households guaranteeing 100 days of wage work.",
        "issuing_authority": "Gram Panchayat / Block Development Office",
        "how_to_obtain": "Submit plain paper application with photos to Panchayat Secretary.",
        "digital_portal_url": "https://nrega.nic.in",
        "common_schemes_count": 8,
        "common_schemes": ["MGNREGA", "PMAY-G", "Rural Livelihoods"]
    },
    {
        "id": "mcp_card",
        "name": "Mother and Child Protection (MCP) Card",
        "name_hi": "मातृ एवं शिशु सुरक्षा कार्ड (एमसीपी कार्ड)",
        "category": "Special Category",
        "description": "Card recording antenatal checkups (ANC), child delivery, birth weight, and complete vaccination cycles.",
        "issuing_authority": "Ministry of Health & Family Welfare / Anganwadi",
        "how_to_obtain": "Issued free upon registering pregnancy at village Anganwadi Centre or Primary Health Centre (PHC).",
        "digital_portal_url": "https://nhm.gov.in",
        "common_schemes_count": 6,
        "common_schemes": ["PMMVY", "Janani Suraksha", "Poshan Abhiyaan"]
    },
    {
        "id": "udyam_registration",
        "name": "Udyam MSME Registration Certificate",
        "name_hi": "उद्यम एमएसएमई पंजीकरण प्रमाण पत्र",
        "category": "Education & Employment",
        "description": "Free zero-cost digital registration certificate for Micro, Small and Medium Enterprises.",
        "issuing_authority": "Ministry of Micro, Small and Medium Enterprises",
        "how_to_obtain": "Register instantly with Aadhaar and PAN on udyamregistration.gov.in.",
        "digital_portal_url": "https://udyamregistration.gov.in",
        "common_schemes_count": 8,
        "common_schemes": ["PM Mudra", "PMEGP", "CGTMSE", "PM Vishwakarma"]
    },
    {
        "id": "education_marksheet",
        "name": "Academic Marksheets & Bonafide Certificate",
        "name_hi": "शैक्षणिक अंकतालिका एवं बोनाफाइड",
        "category": "Education & Employment",
        "description": "Official school/college grade sheets, passing certificates, and enrollment bonafide receipts.",
        "issuing_authority": "Recognized Educational Board / UGC / AICTE University",
        "how_to_obtain": "Available on DigiLocker or from school/college administration.",
        "digital_portal_url": "https://www.digilocker.gov.in",
        "common_schemes_count": 14,
        "common_schemes": ["National Scholarships", "PMKVY", "Pragati Scholarship", "Yuva Nidhi", "Kanyashree"]
    }
]

async def seed_database():
    print("Connecting to MongoDB...")
    # Seed schemes
    await db.schemes.delete_many({})
    dated = 0
    for s in SCHEMES_DATA:
        # Attach the real cut-off window for this scheme; anything not explicitly
        # dated is genuinely open all year and gets an honest ROLLING label.
        deadline = SCHEME_DEADLINES.get(s["id"])
        if deadline is None:
            deadline = {
                "window_type": "ROLLING",
                "note": ROLLING_DEADLINE_NOTES.get(
                    s["id"],
                    "Applications are accepted throughout the year — there is no annual cut-off date.",
                ),
            }
        else:
            dated += 1
        scheme_obj = Scheme(**{**s, "deadline": deadline})
        await db.schemes.insert_one(scheme_obj.model_dump(exclude={"deadline_status"}))
    print(f"Successfully seeded {len(SCHEMES_DATA)} government schemes!")
    print(f"  -> {dated} with real annual/seasonal/event cut-offs, {len(SCHEMES_DATA) - dated} open all year")
    
    # Seed master documents
    await db.master_documents.delete_many({})
    for d in MASTER_DOCUMENTS_DATA:
        doc_obj = MasterDocument(**d)
        await db.master_documents.insert_one(doc_obj.model_dump())
    print(f"Successfully seeded {len(MASTER_DOCUMENTS_DATA)} master citizen documents!")

if __name__ == "__main__":
    asyncio.run(seed_database())
