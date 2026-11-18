\# Real-Time Electronics Sales Analytics and Prediction Platform Using AWS Data Lake



\## Project Overview

This project is an electronics sales analytics and prediction platform that uses AWS S3 to store sales datasets, Python to process and analyze the data, and Machine Learning to forecast future sales.



The platform provides a dashboard to monitor sales performance, analyze product trends, and view sales predictions.



\## Key Features

\- Sales performance dashboard

\- Product and category-wise sales analysis

\- Brand-wise sales analysis

\- Monthly sales trends

\- Machine Learning-based sales prediction

\- AWS S3 data storage

\- Simulated real-time sales feed



\## Technologies Used

\- Python

\- Flask

\- Pandas

\- Scikit-learn

\- Boto3

\- AWS S3

\- HTML

\- CSS

\- JavaScript



\## Project Architecture

Sales Dataset → AWS S3 → Data Processing → Sales Analytics → Machine Learning Prediction → Web Dashboard



\## AWS S3 Structure

```text

electronics-sales-datalake-2026/

│

├── raw/

│   └── electrical\_goods\_sales\_dataset.csv

│

├── processed/

│   └── cleaned\_sales.csv

│

├── predictions/

│   └── sales\_predictions.csv

│

└── realtime/

```



\## Project Files

| File | Description |

|---|---|

| app.py | Flask application and API endpoints |

| analytics.py | Sales analytics |

| process\_data.py | Data processing |

| prediction.py | Sales prediction model |

| test\_s3.py | AWS S3 connection testing |

| index.html | Web dashboard |

| requirements.txt | Python dependencies |



\## Machine Learning

The project uses Linear Regression to forecast future sales based on historical monthly sales data.



\## Installation



1\. Clone the repository:

```bash

git clone https://github.com/venkatsaidoranadula/Electronics-Sales-Analytics-AWS.git

```



2\. Navigate into the project:

```bash

cd Electronics-Sales-Analytics-AWS

```



3\. Install dependencies:

```bash

pip install -r requirements.txt

```



4\. Configure AWS credentials securely using your local AWS credentials configuration.



5\. Run the application:

```bash

python app.py

```



6\. Open the application in your browser:

```text

http://127.0.0.1:5000

```



\## Important Note

The real-time dashboard section uses simulated sales updates. The application runs locally and uses AWS S3 for data storage. AWS credentials are not included in this repository.



\## Author

Venkata Sai Doranadula



B.Tech – Artificial Intelligence and Data Science

