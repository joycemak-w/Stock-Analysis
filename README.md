# Stock Analysis
### Stock analysis of 3 Banks *STAN(2888.HK), HSBC(0005.HK), BOC(2388.HK)* on *Daily Return, Simple Moving Average, Close pirce VS Volume* with GUI and Azure SQL Database
## Environment
-  Create file .env
-  Set your own password and SERVER in .env
## Azure SQL Database
### Schema
| **index**     | **INT IDENTITY(1,1) PRIMARY KEY** |
| ------------- |:-------------:|
| open          | REAL          |
| close         | REAL          |
| volume        | INT           |
| symbol        | NVARCHAR(50) NOT NULL      |

## GUI
<img src="https://github.com/user-attachments/assets/92f733e4-5009-435b-b0be-9cedd1641571" height=400 />

## Functions
- view Daily Reutrn start from 2022/09 of selected stock
- view Simple Moving Average of selected stock and get **Golden/Death Cross**
- view Relationship between close price and volume
- Run **Scheduler** to update Cloud Database(Azure) data
- export plot to png

## Analysis Perspective
<img alt="image" src="https://github.com/user-attachments/assets/b419bbef-ab0d-443d-883b-8181b082c5fe" />

Click comboBox to select the analysis perspective

## Select Stock
<img alt="image" src="https://github.com/user-attachments/assets/86340432-f896-4fd4-9cd6-ac4089e7aacb" />

Tick the box to get that stock' analysis

## Example
<img src="https://github.com/user-attachments/assets/8b424fae-ffc1-4c91-bd0a-6bd5baabf86b" height=400 />




