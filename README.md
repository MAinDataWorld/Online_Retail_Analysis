**# Online Retail II --- Sales Analysis with Python and Power BI**



**## Project Overview**



This project explores historical transaction data from a UK-based online

retailer using Python and Power BI. It follows a reproducible workflow

that starts with the original Excel workbook, prepares a cleaned

transaction-level dataset, performs sales and customer analysis in

Python, generates static visualizations, and presents interactive

findings in a Power BI dashboard.



The analysis focuses on sales trends over time, geographical sales

distribution, product performance in the United Kingdom, order

cancellations, as well as month-over-month (MoM) and year-over-year (YoY) sales

changes.



All monetary values are reported in \*\*British pounds sterling (GBP,

£)\*\*, in accordance with the original dataset.



**## Data Source**



The raw data comes from the **\*\*Online Retail II\*\*** dataset in the UCI

Machine Learning Repository:



\-   **\*\*Dataset:\*\*** [Online Retail II --- UCI Machine Learning

    Repository]\(https\://archive.ics.uci.edu/dataset/502/online+retail+ii)

\-   **\*\*DOI:\*\*** [10.24432/C5CG6D]\(https\://doi.org/10.24432/C5CG6D)

\-   **\*\*Original format:\*\*** Excel workbook containing two worksheets:

    \`Year 2009-2010\` and \`Year 2010-2011\`

\-   **\*\*Original period:\*\*** 1 December 2009 to 9 December 2011

\-   **\*\*Original transaction lines:\*\*** 1,067,371

\-   **\*\*Currency:\*\*** Pound sterling (GBP, £)



The dataset contains transactions from a UK-based, non-store online

retailer. Its fields include invoice numbers, stock codes, product

descriptions, quantities, invoice dates, unit prices, customer

identifiers, and countries.



The source workbook contains incomplete calendar-year coverage at both

ends of the observation period. This is accounted for consistently in

the monthly and yearly analyses, as explained below.

The original Excel workbook is not included in this repository because of its file size. To reproduce the project, download the workbook from the UCI dataset page linked above and place it in the `data/raw/` directory using the filename expected by the cleaning script (`online_retail.xlsx`).

The cleaned transaction-level CSV is also not included because of its file size. It is generated locally by running `01_exploration_and_cleaning.py`, as described in the Reproducibility section.



**## Tools and Technologies**



\-   **\*\*Python\*\*** --- data exploration, cleaning, analysis, and

    visualization

\-   **\*\*Pandas\*\*** --- data manipulation, filtering, and aggregation

\-   **\*\*NumPy\*\*** --- numerical operations

\-   **\*\*Matplotlib\*\*** --- static charts

\-   **\*\*pyjanitor\*\*** --- column-name standardization during data cleaning

\-   **\*\*Power BI\*\*** --- interactive dashboard, KPI cards, filters, and

    visual analysis

\-   **\*\*Git and GitHub\*\*** --- version control and project documentation



**## Repository Structure**



\`\`\` text

Online_Retail_Analysis/
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   │
│   └── processed/
│       └── .gitkeep
│
├── python/
│   ├── 01_exploration_and_cleaning.py
│   └── 02_analysis_and_visualization.py
│
├── figures/
│   ├── 01_monthly_sales_over_time.png
│   ├── 02_yearly_sales.png
│   ├── 03_top_10_countries_december_2009.png
│   ├── 04_top_10_countries_2010.png
│   ├── 05_top_10_countries_2011.png
│   ├── 06_top_10_products_uk.png
│   ├── 07_lowest_10_products_uk.png
│   ├── 08_uk_vs_rest_of_world_sales.png
│   └── 09_monthly_uk_sales.png
│
├── output/
│   ├── month_over_month_analysis.csv
│   └── year_over_year_analysis.csv
│
├── powerbi/
│   ├── retail_analysis.pbix
│   └── screenshots/
│       ├── 01_page_1.png
│       ├── 02_page_2.png
│       ├── 03_page_3.png
│       └── 04_page_4.png
│
└── README.md

\`\`\`



The `data/raw/` and `data/processed/` directories contain `.gitkeep` placeholders because the original Excel workbook and the generated cleaned transaction-level CSV are not uploaded to GitHub due to their file sizes. The cleaned CSV retains the full available date range and cancelled invoices, allowing the project to use the same cleaned source for sales analysis and cancellation analysis. It is created locally by the data-cleaning script.



The Python analysis script exports two additional CSV files:

\`month_over_month_analysis.csv\` and \`year_over_year_analysis.csv\`. These

contain the calculated monthly and yearly sales changes and are also

used in the Power BI report.



**## Project Workflow**



**### 1. Data Exploration and Cleaning**



The first Python script imports both worksheets from the original Excel

workbook and combines them into one dataset.



The main preparation steps are:



1\.  Import both worksheets and concatenate them into a single DataFrame.



2\.  Inspect the dataset dimensions, duplicate records, missing values,

    and data types.



3\.  Remove exact duplicate transaction rows.



4\.  Fill missing product descriptions only when a stock code maps

    unambiguously to one description.



5\.  Convert identifier and description columns to suitable string data

    types.



6\.  Standardize column names to \`snake_case\`.



7\.  Calculate the transaction-line value using:



    \`\`\` python

    total_price = quantity \* price

    \`\`\`



8\.  Export the cleaned dataset as \`cleaned.csv\`.



The original workbook contains **\*\*1,067,371 transaction lines\*\***. After

removing **\*\*34,335 exact duplicate rows\*\***, the cleaned dataset contains

**\*\*1,033,036 rows\*\***.



Missing customer identifiers are retained rather than imputed. Product

descriptions are filled only where the stock-code lookup provides one

unambiguous description; unresolved missing descriptions remain missing.



**### 2. Data Preparation for Sales Analysis**



The second Python script imports \`cleaned.csv\`, converts \`invoice_date\`

to datetime, and extracts year, month, and day fields for time-based

analysis.



**#### Cancelled invoices**



According to the explanation provided by the source of the raw data, cancelled invoices are identified by invoice numbers beginning with the

letter \`C\`.



\-   Cancelled invoices are separated into \`cancelled_orders\`.

\-   They are excluded from the non-cancelled sales dataset used for

    sales calculations.

\-   Negative transaction values in non-cancelled invoices are retained.



Accordingly, the project's sales measure is calculated from

non-cancelled invoices while retaining negative transaction-line values.

It should not be interpreted as a separate accounting reconciliation of

gross sales, refunds, and returns.



**#### Consistent treatment of incomplete months and years**



The same date-inclusion rules are applied throughout the corresponding

monthly and yearly analyses and calculations.



  -----------------------------------------------------------------------

  Analysis          December 2009     December 2011     Period

                                                        represented

  ----------------- ----------------- ----------------- -----------------

  Monthly analysis  Included          Excluded          December

                                                        2009--November

                                                        2011



  Yearly analysis   Excluded          Included through  January 2010--9

                                      9 December        December 2011

  -----------------------------------------------------------------------



**\*\*Monthly analyses\*\*** include December 2009 because it is the only

available month for that calendar year. They exclude December 2011

because the dataset ends on 9 December, making it an incomplete month.



**\*\*Yearly analyses\*\*** exclude December 2009 because the dataset contains

no other months from that year. They retain December 2011, including the

available transactions through 9 December.



These rules are applied to the relevant sales totals, averages, country

comparisons, UK product and monthly sales analyses, quarterly summaries,

and MoM and YoY calculations. December 2009 is treated as a standalone

month in the country analysis, not as a full-year result.



The monthly analysis dataset contains **\*\*989,044 transaction lines\*\***,

covering December 2009 through November 2011. The yearly analysis

dataset contains **\*\*970,223 transaction lines\*\***, covering January 2010

through 9 December 2011.



**### 3. Python Analysis and Visualizations**



The Python analysis script performs the following analyses:



\-   Monthly and yearly sales totals.

\-   Monthly and yearly average transaction-line values.

\-   Country-level sales and top 10 country rankings for December 2009,

    2010, and 2011.

\-   UK-specific monthly sales.

\-   UK product-level sales, including the 10 highest- and 10

    lowest-contributing products.

\-   UK sales compared with the rest of the world.

\-   Quarterly sales summaries based on the included monthly

    observations.

\-   Month-over-month (MoM) and year-over-year (YoY) sales changes.

\-   Unique customer count, order count, and average order value.



The script saves nine Matplotlib figures in the \`figures/\` directory. It

also exports the MoM and YoY analysis tables as separate CSV files in

the \`output/\` directory.



**### 4. Power BI Dashboard**



The Power BI report contains four pages:



  -----------------------------------------------------------------------

  Dashboard page                      Main contents

  ----------------------------------- -----------------------------------

  **\*\*Sales Overview\*\***                  Net sales, number of orders, number

                                      of customers, average sales per

                                      order, and sales trends by month,

                                      year, and quarter; includes a

                                      country filter.



  **\*\*Country & Product Performance\*\***   Sales distribution by country,

                                      orders by country, and

                                      product-level sales comparisons;

                                      includes a year filter.



  **\*\*Order Cancellations\*\***             Cancelled-order count, comparison

                                      of cancelled and non-cancelled

                                      orders, and products associated

                                      with cancelled orders.



  **\*\*Sales Growth (MoM & YoY)\*\***        Month-over-month and year-over-year

                                      sales growth analysis, supported by

                                      the Python-generated MoM and YoY

                                      CSV files.

  -----------------------------------------------------------------------



The Power BI report uses the cleaned transaction-level data together

with the two exported MoM and YoY analysis tables. The monthly and

yearly visuals and calculations follow the date-inclusion rules

described above. The cancellation analysis uses the cancelled invoices

separated from the complete cleaned dataset.

The repository also includes screenshots of the four dashboard pages in `powerbi/screenshots/` for a quick preview without opening the Power BI file.

![Power BI Page 1](powerbi/screenshots/01_page_1.png)

![Power BI Page 2](powerbi/screenshots/01_page_2.png)

![Power BI Page 3](powerbi/screenshots/01_page_3.png)

![Power BI Page 4](powerbi/screenshots/01_page_4.png)



**## Key Findings and Business Insights**



**### 1. Sales Are Highly Concentrated in the United Kingdom**



Across the monthly-analysis period (December 2009--November 2011), total

net sales were **\*\*£19,679,775.98\*\***.



The United Kingdom contributed **\*\*£16,659,900.24\*\***, representing

**\*\*84.65%\*\*** of total net sales. All other countries combined contributed

**\*\*£3,019,875.74 (15.35%)\*\***.



  Market                         Net sales   Share of net sales

  ------------------- -------------------- --------------------

  United Kingdom            £16,659,900.24               84.65%

  Rest of the world          £3,019,875.74               15.35%

  **\*\*Total\*\***             **\*\*£19,679,775.98\*\***          **\*\*100.00%\*\***



The UK's sales contribution was approximately 5.52 times that of all

other countries combined.



The largest non-UK markets over the monthly-analysis period were:



  Country           Net sales

  ------------- -------------

  EIRE            £651,426.42

  Netherlands     £542,310.07

  Germany         £417,035.54

  France          £343,161.17

  Australia       £169,283.46



The retailer's strong UK concentration is consistent with the business

being UK-based. The international sales contribution also provides a

basis for investigating opportunities in other markets. However, the

available transaction data does not establish why sales differ between

countries. It does not include marketing expenditure, website traffic,

conversion rates, market size, or shipping costs.



**### 2. Country Rankings Differ Across the Observed Periods**



The country rankings are calculated using the appropriate analysis

period: December 2009 is presented separately, while 2010 and 2011 use

the yearly dataset. The 2011 results include transactions through 9

December only.



**\*\*December 2009 --- top 10 countries\*\***



    Rank Country              Net sales

  ------ ---------------- -------------

       1 United Kingdom     £747,397.29

       2 EIRE                £20,099.74

       3 Netherlands         £15,204.73

       4 Germany              £9,830.27

       5 Spain                £7,950.18

       6 France               £6,521.69

       7 Cyprus               £3,541.68

       8 Portugal             £2,821.58

       9 Austria              £1,998.34

      10 Denmark              £1,437.66



**\*\*2010 --- top 10 countries\*\***



    Rank Country                Net sales

  ------ ---------------- ---------------

       1 United Kingdom     £8,270,584.93

       2 EIRE                 £365,560.31

       3 Netherlands          £262,171.50

       4 Germany              £201,716.78

       5 France               £143,907.34

       6 Sweden                £57,050.99

       7 Denmark               £49,469.19

       8 Switzerland           £44,333.51

       9 Spain                 £40,667.48

      10 Australia             £31,523.90



**\*\*2011 --- top 10 countries (through 9 December)\*\***



    Rank Country                Net sales

  ------ ---------------- ---------------

       1 United Kingdom     £8,233,537.75

       2 Netherlands          £276,661.86

       3 EIRE                 £273,107.26

       4 Germany              £213,472.66

       5 France               £200,027.06

       6 Australia            £137,488.46

       7 Spain                 £59,714.83

       8 Switzerland           £55,762.68

       9 Belgium               £39,386.43

      10 Sweden                £34,533.53



December 2009 represents a single month and must not be interpreted as a

full-year country comparison. Similarly, 2011 country totals represent

an incomplete year.



**### 3. Sales Were Highest in the Observed Fourth-Quarter Months**



**### Quarterly Sales Analysis**



Net sales were grouped by calendar quarter in Power BI using the **\*\*complete cleaned dataset\*\***, without applying the separate date filters used for the monthly and yearly analyses. The figures therefore reflect all non-cancelled net sales available in the dataset, including transactions from December 2009 and December 2011.



\| Quarter | Net sales | Average monthly net sales |

\|:---:|---:|---:|

\| Q1 | £3,962,147.53 | £660,357.92 |

\| Q2 | £4,099,335.81 | £683,222.64 |

\| Q3 | £4,731,955.95 | £788,659.33 |

\| Q4 | £6,886,336.68 | £1,147,722.78 |



Average monthly net sales in Q4 were approximately **\*\*73.80% higher than in Q1\*\***.



This comparison is descriptive and should not be interpreted as a formal seasonal analysis. The quarterly figures are based on the available transactions in the cleaned dataset, which does not cover complete calendar years at both ends of the observation period.



**### 4. A Small Group of Products Contributes Meaningfully to UK Sales**



The UK product analysis excludes stock codes associated with fees,

adjustments, postage, and test entries. Remaining UK transactions are

grouped by product description, and the 10 products with the highest net

sales are identified.



    Rank Product description                       Net sales

  ------ ------------------------------------- -------------

       1 REGENCY CAKESTAND 3 TIER                £273,257.65

       2 WHITE HANGING HEART T-LIGHT HOLDER      £238,879.75

       3 PARTY BUNTING                           £138,586.55

       4 JUMBO BAG RED RETROSPOT                 £133,774.16

       5 ASSORTED COLOUR BIRD ORNAMENT           £118,019.31

       6 PAPER CHAIN KIT 50'S CHRISTMAS          £107,859.28

       7 MEDIUM CERAMIC TOP STORAGE JAR           £80,372.84

       8 CHILLI LIGHTS                            £76,813.04

       9 ROTATING SILVER ANGELS T-LIGHT HLDR      £65,980.47

      10 JUMBO BAG STRAWBERRY                     £64,684.29



Together, the top 10 products generated **\*\*£1,298,227.34\*\***, approximately

**\*\*8.00% of net sales in the included UK product records\*\***.



These products may warrant closer attention when reviewing product

availability, replenishment, and production planning. Their historical

sales contribution is a useful starting point, but decisions should also

consider costs, profit margins, inventory, supplier constraints, and

future demand.



**### 5. The Lowest-Contributing UK Products May Warrant Further Review**



The analysis also identifies the 10 products with the lowest

**\*\*positive\*\*** net sales in the UK over the monthly-analysis period.



  Product description                     Net sales

  ------------------------------------- -----------

  PADS TO MATCH ALL CUSHIONS                  £0.02

  HAPPY BIRTHDAY GINGER CAT CARD              £0.38

  PINK HEART CHRISTMAS DECORATION             £0.38

  CAT W SUNGLASSES BLANK CARD                 £0.76

  OWLS CHARLOTTE BAG                          £0.85

  CAT WITH SUNGLASSES BLANK CARD              £0.95

  HAPPY BIRTHDAY CARD TEDDY/CAKE              £1.14

  FOLKART HEART CHRISTMAS DECORATIONS         £1.25

  HOLLYHOCK SQUARE HANDY TIN                  £1.25

  LETTER "U" BLING KEY RING                   £1.25



These products could be reviewed to understand whether their low

recorded sales reflect limited demand, seasonal relevance, restricted

availability, or other factors. Low sales alone do not establish that a

product is unprofitable or should be discontinued; cost and inventory

information would be needed for such decisions.



**### 6. Order, Customer, and Cancellation Metrics**



For the monthly-analysis period (December 2009--November 2011), the

non-cancelled sales dataset contained:



  Metric                           Result

  ----------------------------- ---------

  Non-cancelled orders             44,467

  Identified unique customers       5,853

  Average order value             £442.57

  Countries represented                43



Average order value is calculated by first summing transaction-line

values within each non-cancelled invoice and then averaging those

invoice totals. Customer count is based on non-missing customer IDs.



Across the complete cleaned dataset, the cancellation analysis

identified **\*\*19,104 cancelled transaction lines\*\***, corresponding to

**\*\*8,292 distinct cancelled invoices\*\***. The complete dataset also

contains **\*\*45,336 distinct non-cancelled invoices\*\***. These cancellation

counts use the complete available dataset rather than the restricted

monthly-analysis period.



**### 7. Yearly Sales and YoY Change**



The yearly analysis excludes December 2009 and retains the available

December 2011 transactions through 9 December.



  Year         Net sales

  ------ ---------------

  2010     £9,696,548.40

  2011     £9,798,551.95



The calculated YoY change from 2010 to 2011 is **\*\*+1.05%\*\***.



This is not a like-for-like comparison of two complete calendar years:

2010 contains a full year of data, whereas 2011 ends on 9 December. The

percentage should therefore be interpreted as a comparison of the

available yearly totals, not as a definitive measure of full-year

growth.



**## Python Visualizations**



The Python script generates the following figures:



**### 1. Monthly Sales Over Time**



![Monthly sales over time]\(figures/01_monthly_sales_over_time.png)



**### 2. Yearly Sales**



![Yearly sales]\(figures/02_yearly_sales.png)



**### 3. Top 10 Countries --- December 2009**



![Top 10 countries in December

2009]\(figures/03_top_10_countries_december_2009.png)



**### 4. Top 10 Countries --- 2010**



![Top 10 countries in 2010]\(figures/04_top_10_countries_2010.png)



**### 5. Top 10 Countries --- 2011**



![Top 10 countries in 2011]\(figures/05_top_10_countries_2011.png)



**### 6. Top 10 Products in the UK**



![Top 10 products in the UK]\(figures/06_top_10_products_uk.png)



**### 7. Lowest 10 Positive-Sales Products in the UK**



![Lowest 10 products in the UK]\(figures/07_lowest_10_products_uk.png)



**### 8. UK vs. Rest of the World**



![UK versus rest of the world

sales]\(figures/08_uk_vs_rest_of_world_sales.png)



**### 9. Monthly UK Sales**



![Monthly UK sales]\(figures/09_monthly_uk_sales.png)



**## Limitations and Considerations**



1\.  **\*\*Partial coverage of 2009:\*\*** The dataset contains only December

    2009 for that calendar year, with transactions beginning on 1

    December. It is included in monthly analysis and treated as a

    standalone period in the country analysis, but excluded from yearly

    totals. It should not be interpreted as a complete year.



2\.  **\*\*Incomplete December 2011:\*\*** The dataset ends on 9 December 2011.

    December 2011 is excluded from monthly analyses but retained in

    yearly analyses. Consequently, 2011 yearly totals and country

    rankings are incomplete.



3\.  **\*\*Cancelled invoices and sales definition:\*\*** Invoices beginning with

    \`C\` are separated and excluded from non-cancelled sales

    calculations. Negative values in non-cancelled transaction lines are

    retained. The project's net-sales measure is therefore based on

    non-cancelled invoices while preserving negative transaction values;

    it is not a separate accounting reconciliation of all returns and

    refunds.



4\.  **\*\*Missing customer identifiers:\*\*** The cleaned dataset contains

    **\*\*235,151 missing customer IDs\*\***. These records remain in sales

    calculations, but they cannot contribute to the distinct

    identified-customer count. Customer-level findings should be

    interpreted accordingly.



5\.  **\*\*Missing product descriptions:\*\*** The cleaned dataset contains

    **\*\*1,301 missing product descriptions\*\*** after the

    description-recovery step. Descriptions are filled only when a stock

    code maps to one unique description. Product-level analysis based on

    descriptions cannot fully represent records whose descriptions

    remain missing.



6\.  **\*\*Product rankings are based on sales, not profitability:\*\*** The top

    and lowest product rankings use net sales values, not profit

    margins. The lowest-product list includes only products with

    positive net sales and excludes non-product stock codes such as

    postage, fees, adjustments, and test entries. It does not establish

    that these products are unprofitable or should be discontinued.



7\.  **\*\*Limited explanatory variables:\*\*** The dataset does not include

    marketing expenditure, website visits, conversion rates, product

    costs, profit margins, inventory availability, or shipping costs.

    The analysis can identify patterns and opportunities, but it cannot

    establish the causes of sales differences or measure marketing

    effectiveness.



8\.  **\*\*Historical and business-specific data:\*\*** The dataset covers a

    limited historical period and one UK-based retailer. The results

    should not be assumed to represent current retail conditions or

    other businesses.



**## Conclusion**



This project demonstrates how transaction-level retail data can be

prepared, analyzed, and communicated using Python and Power BI. The

analysis identifies a strong concentration of sales in the United

Kingdom, differences in sales across countries and products, higher

average sales in the observed Q4 months, and measurable order

cancellations.



The findings provide a starting point for further business

investigation, including international market development, product

assortment and replenishment reviews, and closer examination of sales

patterns. These decisions would benefit from additional information on

profitability, marketing activity, customer behavior, and inventory.



Combining Python-based preparation and analysis with an interactive

Power BI dashboard provides a reproducible workflow and an accessible

way to explore the results.



**## Reproducibility**



To reproduce the analysis:



1\.  Clone or download the repository.



2\.  Download the original **Online Retail II** workbook from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii) and place it at `data/raw/online_retail.xlsx`. The original workbook is not included in this repository.\`.



3\.  Install the required Python libraries:



    \`\`\` bash

    pip install pandas numpy matplotlib pyjanitor openpyxl

    \`\`\`



4\.  Run the scripts in order from the project root:



    \`\`\` bash

    python python/01_exploration_and_cleaning.py

    python python/02_analysis_and_visualization.py

    \`\`\`



5\.  Open \`powerbi/retail_analysis.pbix\` in Power BI Desktop to explore

    the dashboard.



The analysis script depends on the \`cleaned.csv\` file generated by the

cleaning script. It generates the figures and the two analysis CSV files

used for MoM and YoY reporting.



**## Acknowledgements**



Chen, D. (2012). *\*Online Retail II\** \\[Dataset\\]. UCI Machine Learning

Repository. https\://doi.org/10.24432/C5CG6D.



The dataset is distributed under the Creative Commons Attribution 4.0

International (CC BY 4.0) license. Please retain appropriate attribution

when reusing or redistributing the dataset.
