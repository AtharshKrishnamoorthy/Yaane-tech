from pydantic import BaseModel, Field
from typing import List, Optional

class CrimeCategories:
    MAIN_CATEGORIES = [
        "Women/Child Related Crime",
        "Financial Fraud Crimes",
        "Other Cyber Crime"
    ]
    
    SUBCATEGORIES = {
        "Women/Child Related Crime": [
            "Child Pornography/Child Sexual Abuse Material (CSAM)",
            "Rape/Gang Rape-Sexually Abusive Content",
            "Sale, Publishing and Transmitting Obscene Material/Sexually Explicit Material",
            "Cyber Bullying/Stalking/Sexting"
        ],
        "Financial Fraud Crimes": [
            "Debit/Credit Card Fraud",
            "SIM Swap Fraud",
            "Internet Banking-Related Fraud",
            "Business Email Compromise/Email Takeover",
            "E-Wallet Related Frauds",
            "FraudCall/Vishing",
            "Demat/Depository Fraud",
            "UPI-Related Frauds",
            "Aadhaar Enabled Payment System(AEPS) Fraud",
            "Online Job Fraud",
            "Online Matrimonial Fraud",
            "Online Gambling/Betting Fraud",
            "Cryptocurrency Crime"
        ],
        "Other Cyber Crime": [
            "EmailPhishing",
            "Cheating by Impersonation",
            "Fake/Impersonating Profile",
            "Profile Hacking/Identity Theft",
            "Provocative Speech of Unlawful Acts",
            "Impersonating Email",
            "Intimidating Email",
            "EmailHacking",
            "Damage to Computer Systems",
            "Tampering with Computer Source Documents",
            "Defacement/Hacking",
            "Unauthorized Access/Data Breach",
            "Online Cyber Trafficking",
            "Ransomware",
            "Cyber Terrorism"
        ]
    }

class LegalResponse(BaseModel):
    title: str = Field(..., description="Crime category/type with 'in India: A Guide' suffix")
    introduction: str = Field(..., description="Comprehensive overview of the crime")
    severity: str = Field(..., description="Detailed impact analysis with bullet points")
    applicable_laws: List[str] = Field(..., description="All relevant laws and sections")
    reporting: str = Field(..., description="Help and reporting procedures")
    penalties: str = Field(..., description="Detailed punishment information")
    sources: List[str] = Field(..., description="List of references and sources")