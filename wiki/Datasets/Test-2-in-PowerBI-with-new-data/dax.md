



# DAX

|Dataset|[Test 2 in PowerBI with new data](./../Test-2-in-PowerBI-with-new-data.md)|
| :--- | :--- |
|Workspace|[Intranet usage](../../Workspaces/Intranet-usage.md)|

## Table: Table1

### Measures:


```dax
Count of Item total for Item = 
CALCULATE(COUNTA('Table1'[Item]), ALLSELECTED('Table1'[Item]))
```


### Calculated Columns:


```dax
Position (groups) = SWITCH(
	TRUE,
	ISBLANK('Table1'[Position]),
	"(Blank)",
	'Table1'[Position] IN {"Analyst",
		"Business Analyst",
		"Consulting Analyst",
		"Intern"},
	"Analyst or intern",
	'Table1'[Position] IN {"Consultant",
		"Junior Consultant",
		"Senior Consultant"},
	"Consultant",
	'Table1'[Position] IN {"Consultant-FL",
		"Consultant-FLS",
		"Freelancer Services FL",
		"Freelancer Services FLS",
		"Partner-FL",
		"Post Graduate",
		"Senior Advisor-FL",
		"Senior Advisor-FLS",
		"Subcontractor",
		"Subcontractor Consulting.",
		"Subcontractor IT.",
		"Subcontractor."},
	"Freelancer or postgraduate",
	'Table1'[Position] IN {"Apprentice Services",
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
	"Group Function",
	'Table1'[Position] IN {"Director",
		"Partner",
		"Principal"},
	"Partner, Principal, Director",
	'Table1'[Position] IN {"Polarix"},
	"Polarix",
	'Table1'[Position] IN {"Project Manager"},
	"Project Manager",
	"Other"
)
```



```dax
Country (groups) = SWITCH(
	TRUE,
	ISBLANK('Table1'[Country]),
	"(Blank)",
	'Table1'[Country] IN {"Brazil",
		"Canada",
		"USA"},
	"Americas",
	'Table1'[Country] IN {"Austria",
		"Germany",
		"Polarix",
		"Switzerland"},
	"DACH",
	'Table1'[Country] IN {"Hungary",
		"Romania",
		"Russia",
		"Ukraine"},
	"Eastern Europe",
	'Table1'[Country] IN {"France",
		"Morocco"},
	"France & Morocco",
	'Table1'[Country] IN {"China",
		"Hong Kong"},
	"Greater China",
	'Table1'[Country] IN {"India",
		"Japan",
		"Korea, Republic of"},
	"Japan, India, Korea",
	'Table1'[Country] IN {"Italy",
		"Portugal",
		"Spain"},
	"Mediterranean Europe",
	'Table1'[Country] IN {"Bahrain",
		"Lebanon",
		"Qatar",
		"Saudi Arabia",
		"United Arab Emirates"},
	"Middle East",
	'Table1'[Country] IN {"Belgium",
		"Netherlands",
		"Sweden",
		"United Kingdom"},
	"Northern Europe",
	'Table1'[Country] IN {"Indonesia",
		"Malaysia",
		"Singapore",
		"Thailand",
		"Viet Nam"},
	"SEA",
	"Other"
)
```



```dax
Item = 1
```

