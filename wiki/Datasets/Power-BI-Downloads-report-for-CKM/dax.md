



# DAX

|Dataset|[Power BI Downloads report for CKM](./../Power-BI-Downloads-report-for-CKM.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: Confidential

### Calculated Columns:


```dax
Position (groups) = SWITCH(
	TRUE,
	ISBLANK('Confidential'[Position]),
	"(Blank)",
	'Confidential'[Position] IN {"Analyst",
		"Business Analyst",
		"Consulting Analyst",
		"Intern"},
	"Analyst or intern",
	'Confidential'[Position] IN {"Consultant",
		"Junior Consultant",
		"Senior Consultant"},
	"Consultant",
	'Confidential'[Position] IN {"Consultant-FL",
		"Consultant-FLS",
		"Freelancer Services FL",
		"Freelancer Services FLS",
		"Partner-FL",
		"Post Graduate",
		"Senior Advisor",
		"Senior Advisor-FL",
		"Senior Advisor-FLS",
		"Subcontractor",
		"Subcontractor Consulting.",
		"Subcontractor IT.",
		"Subcontractor."},
	"Freelancers or postgraduates or subscontractors",
	'Confidential'[Position] IN {"Apprentice Services",
		"Cons. Junior Specialist",
		"Cons. Manager",
		"Cons. Senior Expert",
		"Cons. Senior Manager",
		"Cons. Senior Specialist",
		"Cons. Specialist",
		"CSS Principal",
		"Expert",
		"HR Principal",
		"Intern Services",
		"Junior Specialist",
		"Manager",
		"Office Manager",
		"Personal Assistant",
		"Project Manager Group Function",
		"Senior Expert",
		"Senior Personal Assistant",
		"Senior Specialist",
		"Senior Vice President",
		"Specialist",
		"Team Personal Assistant",
		"Temp Help Services"},
	"Group Functions",
	'Confidential'[Position] IN {"Chief of Staff",
		"Director",
		"Partner",
		"Principal"},
	"P/PI/Director/CoS",
	'Confidential'[Position] IN {"Project Manager"},
	"Project Manager",
	"Other"
)
```



```dax
Country (groups) = SWITCH(
	TRUE,
	ISBLANK('Confidential'[Country]),
	"(Blank)",
	'Confidential'[Country] IN {"Brazil",
		"Canada",
		"Mexico",
		"USA"},
	"Americas",
	'Confidential'[Country] IN {"Austria",
		"Germany",
		"Switzerland"},
	"DACH",
	'Confidential'[Country] IN {"Hungary",
		"Romania",
		"Russia",
		"Ukraine"},
	"Eastern Europe",
	'Confidential'[Country] IN {"France",
		"Morocco"},
	"France & Morocco",
	'Confidential'[Country] IN {"China",
		"Hong Kong"},
	"Greater China",
	'Confidential'[Country] IN {"India",
		"Japan",
		"Korea, Republic of"},
	"Japan & Korea & India",
	'Confidential'[Country] IN {"Italy",
		"Portugal",
		"Spain"},
	"Mediterranean Europe",
	'Confidential'[Country] IN {"Bahrain",
		"Lebanon",
		"Qatar",
		"Saudi Arabia",
		"United Arab Emirates"},
	"Middle East",
	'Confidential'[Country] IN {"Belgium",
		"Netherlands",
		"Sweden",
		"United Kingdom"},
	"Northern Europe",
	'Confidential'[Country] IN {"0",
		"Not available"},
	"Not available",
	'Confidential'[Country] IN {"Indonesia",
		"Malaysia",
		"Singapore",
		"Thailand",
		"Viet Nam"},
	"SEA",
	'Confidential'[Country]
)
```

