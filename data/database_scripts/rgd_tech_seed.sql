-- RGD Tech Enterprise Hybrid RAG
-- Seed data for the final ALC model.
SET search_path TO rgd;

INSERT INTO customers VALUES
('C001','Aarav','Sharma','aarav.sharma@example.com','9000000001','consumer','active','2025-02-12'),
('C002','Priya','Mehta','priya.mehta@example.com','9000000002','consumer','active','2025-03-18'),
('C003','Rohan','Verma','rohan.verma@example.com','9000000003','consumer','active','2025-05-06'),
('C004','Neha','Patel','neha.patel@example.com','9000000004','consumer','active','2025-06-21'),
('C005','Vikram','Singh','vikram.singh@example.com','9000000005','business','active','2025-07-11'),
('C006','Ananya','Rao','ananya.rao@example.com','9000000006','consumer','active','2025-08-02'),
('C007','Kabir','Joshi','kabir.joshi@example.com','9000000007','consumer','active','2025-09-15'),
('C008','Ishita','Nair','ishita.nair@example.com','9000000008','business','active','2025-10-04'),
('C009','Aditya','Kapoor','aditya.kapoor@example.com','9000000009','consumer','active','2025-11-19'),
('C010','Meera','Iyer','meera.iyer@example.com','9000000010','consumer','active','2025-12-08'),
('C011','Rahul','Das','rahul.das@example.com','9000000011','consumer','active','2026-01-13'),
('C012','Sneha','Kulkarni','sneha.kulkarni@example.com','9000000012','consumer','active','2026-02-20');

INSERT INTO products VALUES
('P001','NMP15-2026','RGD ProBook 15','laptop',74999,24,'active'),
('P002','NMAX-2026','RGD UltraBook X','laptop',99999,24,'active'),
('P003','NMP14-2026','RGD ProBook 14','laptop',67999,24,'active'),
('P004','NRX1-2026','RGD Phone X1','smartphone',44999,12,'active'),
('P005','NRX1P-2026','RGD Phone X1 Pro','smartphone',64999,12,'active'),
('P006','NPL-2026','RGD Phone Lite','smartphone',24999,12,'active'),
('P007','NT10-2026','RGD Tab 10','tablet',32999,12,'active'),
('P008','NTP-2026','RGD Tab Pro','tablet',54999,12,'active'),
('P009','NMW-2026','RGD Mouse Wireless','accessory',1999,6,'active'),
('P010','NBP-2026','RGD Bag Pro','accessory',3999,6,'active');

INSERT INTO orders VALUES
('O1001','C001','2026-07-01','delivered',74999,'paid','delivered'),
('O1002','C002','2026-07-03','delivered',44999,'paid','delivered'),
('O1003','C003','2026-07-05','delivered',67999,'paid','delivered'),
('O1004','C004','2026-07-08','delivered',64999,'paid','delivered'),
('O1005','C005','2026-07-10','delivered',99999,'paid','delivered'),
('O1006','C006','2026-07-12','delivered',32999,'paid','delivered'),
('O1007','C007','2026-07-15','shipped',54999,'paid','in_transit'),
('O1008','C003','2026-07-18','delivered',74999,'paid','delivered'),
('O1009','C008','2026-07-20','delivered',44999,'paid','delivered'),
('O1010','C009','2026-07-22','cancelled',24999,'refunded','cancelled'),
('O1011','C010','2026-07-24','delivered',1999,'paid','delivered'),
('O1012','C011','2026-07-25','delivered',3999,'paid','delivered'),
('O1013','C012','2026-07-27','processing',54999,'paid','pending'),
('O1014','C001','2026-07-28','delivered',44999,'paid','delivered'),
('O1015','C002','2026-07-29','delivered',32999,'paid','delivered'),
('O1016','C004','2026-07-30','delivered',74999,'paid','delivered'),
('O1017','C005','2026-08-01','delivered',64999,'paid','delivered'),
('O1018','C006','2026-08-02','delivered',24999,'paid','delivered'),
('O1019','C007','2026-08-03','processing',99999,'paid','pending'),
('O1020','C008','2026-08-04','delivered',67999,'paid','delivered'),
('O1021','C009','2026-08-05','delivered',44999,'paid','delivered'),
('O1022','C010','2026-08-06','delivered',32999,'paid','delivered'),
('O1023','C011','2026-08-07','delivered',74999,'paid','delivered'),
('O1024','C012','2026-08-08','delivered',64999,'paid','delivered'),
('O1025','C003','2026-08-09','delivered',24999,'paid','delivered');

INSERT INTO order_items VALUES
('OI001','O1001','P001',1,74999,0),('OI002','O1002','P004',1,44999,0),
('OI003','O1003','P003',1,67999,0),('OI004','O1004','P005',1,64999,0),
('OI005','O1005','P002',1,99999,0),('OI006','O1006','P007',1,32999,0),
('OI007','O1007','P008',1,54999,0),('OI008','O1008','P001',1,74999,0),
('OI009','O1009','P004',1,44999,0),('OI010','O1010','P006',1,24999,0),
('OI011','O1011','P009',1,1999,0),('OI012','O1012','P010',1,3999,0),
('OI013','O1013','P008',1,54999,0),('OI014','O1014','P004',1,44999,0),
('OI015','O1015','P007',1,32999,0),('OI016','O1016','P001',1,74999,0),
('OI017','O1017','P005',1,64999,0),('OI018','O1018','P006',1,24999,0),
('OI019','O1019','P002',1,99999,0),('OI020','O1020','P003',1,67999,0),
('OI021','O1021','P004',1,44999,0),('OI022','O1022','P007',1,32999,0),
('OI023','O1023','P001',1,74999,0),('OI024','O1024','P005',1,64999,0),
('OI025','O1025','P006',1,24999,0);

INSERT INTO payments VALUES
('PAY001','O1001','credit_card',74999,'success','2026-07-01'),
('PAY002','O1002','upi',44999,'success','2026-07-03'),
('PAY003','O1003','credit_card',67999,'success','2026-07-05'),
('PAY004','O1004','upi',64999,'success','2026-07-08'),
('PAY005','O1005','net_banking',99999,'success','2026-07-10'),
('PAY006','O1006','credit_card',32999,'success','2026-07-12'),
('PAY007','O1007','upi',54999,'success','2026-07-15'),
('PAY008','O1008','credit_card',74999,'success','2026-07-18'),
('PAY009','O1009','upi',44999,'success','2026-07-20'),
('PAY010','O1010','credit_card',24999,'refunded','2026-07-22'),
('PAY011','O1011','upi',1999,'success','2026-07-24'),
('PAY012','O1012','upi',3999,'success','2026-07-25'),
('PAY013','O1013','credit_card',54999,'success','2026-07-27'),
('PAY014','O1014','upi',44999,'success','2026-07-28'),
('PAY015','O1015','credit_card',32999,'success','2026-07-29'),
('PAY016','O1016','credit_card',74999,'success','2026-07-30'),
('PAY017','O1017','upi',64999,'success','2026-08-01'),
('PAY018','O1018','upi',24999,'success','2026-08-02'),
('PAY019','O1019','credit_card',99999,'success','2026-08-03'),
('PAY020','O1020','net_banking',67999,'success','2026-08-04'),
('PAY021','O1021','upi',44999,'success','2026-08-05'),
('PAY022','O1022','credit_card',32999,'success','2026-08-06'),
('PAY023','O1023','credit_card',74999,'success','2026-08-07'),
('PAY024','O1024','upi',64999,'success','2026-08-08'),
('PAY025','O1025','upi',24999,'success','2026-08-09');

INSERT INTO shipments VALUES
('S001','O1001','RGD Logistics','RGD100001','2026-07-02','2026-07-06','2026-07-05','delivered'),
('S002','O1002','BlueDart','RGD100002','2026-07-04','2026-07-08','2026-07-07','delivered'),
('S003','O1003','Delhivery','RGD100003','2026-07-06','2026-07-10','2026-07-10','delivered'),
('S004','O1004','BlueDart','RGD100004','2026-07-09','2026-07-13','2026-07-12','delivered'),
('S005','O1005','Delhivery','RGD100005','2026-07-11','2026-07-16','2026-07-15','delivered'),
('S006','O1006','RGD Logistics','RGD100006','2026-07-13','2026-07-17','2026-07-16','delivered'),
('S007','O1007','BlueDart','RGD100007','2026-07-16','2026-07-20',NULL,'in_transit'),
('S008','O1008','Delhivery','RGD100008','2026-07-19','2026-07-23','2026-07-22','delivered'),
('S009','O1009','BlueDart','RGD100009','2026-07-21','2026-07-25','2026-07-24','delivered'),
('S010','O1011','RGD Logistics','RGD100011','2026-07-25','2026-07-28','2026-07-27','delivered'),
('S011','O1012','BlueDart','RGD100012','2026-07-26','2026-07-30','2026-07-29','delivered'),
('S012','O1013','Delhivery','RGD100013',NULL,'2026-08-12',NULL,'pending'),
('S013','O1014','BlueDart','RGD100014','2026-07-29','2026-08-02','2026-08-01','delivered'),
('S014','O1015','RGD Logistics','RGD100015','2026-07-30','2026-08-03','2026-08-02','delivered'),
('S015','O1016','Delhivery','RGD100016','2026-07-31','2026-08-04','2026-08-03','delivered'),
('S016','O1017','BlueDart','RGD100017','2026-08-02','2026-08-06','2026-08-05','delivered'),
('S017','O1018','RGD Logistics','RGD100018','2026-08-03','2026-08-07','2026-08-06','delivered'),
('S018','O1019','Delhivery','RGD100019',NULL,'2026-08-11',NULL,'pending'),
('S019','O1020','BlueDart','RGD100020','2026-08-05','2026-08-09','2026-08-08','delivered'),
('S020','O1021','RGD Logistics','RGD100021','2026-08-06','2026-08-10','2026-08-09','delivered');

INSERT INTO returns VALUES
('R001','O1001','OI001','customer changed mind','2026-07-18','approved','sealed packaging'),
('R002','O1003','OI003','performance issue','2026-07-20','approved','defect confirmed'),
('R003','O1004','OI004','wrong product received','2026-07-15','completed','wrong model verified'),
('R004','O1008','OI008','overheating issue','2026-08-01','under_inspection','diagnostic pending'),
('R005','O1010','OI010','order cancelled before shipment','2026-07-22','completed','not shipped'),
('R006','O1017','OI017','battery issue','2026-08-10','approved','battery fault confirmed'),
('R007','O1021','OI021','customer changed mind','2026-08-12','rejected','return window exceeded'),
('R008','O1023','OI023','display issue','2026-08-11','approved','defect confirmed');

INSERT INTO refunds VALUES
('RF001','R001','PAY001',74999,'processed','2026-07-25'),
('RF002','R002','PAY003',67999,'processed','2026-07-28'),
('RF003','R003','PAY004',64999,'processed','2026-07-21'),
('RF004','R005','PAY010',24999,'processed','2026-07-24'),
('RF005','R006','PAY017',64999,'pending',NULL),
('RF006','R008','PAY023',74999,'pending',NULL);

INSERT INTO warehouses VALUES
('W001','West Hub','Mumbai'),
('W002','Central Hub','Nagpur');

INSERT INTO inventory VALUES
('P001','W001',18,3,5),('P002','W001',7,2,3),('P003','W001',14,1,4),
('P004','W001',22,4,6),('P005','W001',9,2,4),('P006','W002',30,5,8),
('P007','W002',16,2,5),('P008','W002',8,3,4),('P009','W002',45,6,10),
('P010','W002',27,4,8);

-- Final two-role model: support/admin.
-- Internal finance/operations personnel are represented as admin because
-- the application has only two authorization roles.
INSERT INTO employees VALUES
('E001','Arjun Malhotra','Customer Support','Support Agent','support','active'),
('E002','Kavya Shah','Customer Support','Senior Support Agent','support','active'),
('E003','Manish Gupta','Finance','Finance Analyst','admin','active'),
('E004','Divya Menon','Operations','Operations Manager','admin','active'),
('E005','Siddharth Jain','Technical Support','Technical Specialist','support','active'),
('E006','Pooja Bansal','Finance','Finance Manager','admin','active'),
('E007','Nitin Rao','Administration','System Administrator','admin','active');

-- Support-accessible PDFs.
INSERT INTO documents VALUES
('DOC001','refund_policy_2026.pdf','refund_policy','finance','2026.1','2026-07-01','support','active'),
('DOC002','return_policy_2026.pdf','return_policy','operations','2026.1','2026-07-01','support','active'),
('DOC003','shipping_policy_2026.pdf','shipping_policy','operations','2026.1','2026-07-01','support','active'),
('DOC004','warranty_policy_2026.pdf','warranty_policy','support','2026.1','2026-07-01','support','active'),
('DOC005','cancellation_policy_2026.pdf','cancellation_policy','operations','2026.1','2026-07-01','support','active'),
('DOC006','payment_policy_2026.pdf','payment_policy','finance','2026.1','2026-07-01','support','active'),
('DOC007','product_catalog_2026.pdf','product_catalog','operations','2026.1','2026-07-01','support','active'),
('DOC008','customer_support_policy.pdf','support_policy','support','2026.1','2026-07-01','support','active'),
('DOC009','troubleshooting_guide.pdf','troubleshooting','support','2026.1','2026-07-01','support','active');

-- Admin-only PDFs created for the ALC demonstration.
INSERT INTO documents VALUES
('DOC010','DOC010_internal_financial_operations.pdf','internal_financial_operations','finance','2026.1','2026-07-01','admin','active'),
('DOC011','DOC011_internal_inventory_strategy.pdf','internal_inventory_strategy','operations','2026.1','2026-07-01','admin','active'),
('DOC012','DOC012_internal_employee_compensation.pdf','internal_employee_compensation','human_resources','2026.1','2026-07-01','admin','active');

-- Demo chunk registry records.
-- The ingestion pipeline will later replace/extend these with real chunk records
-- generated from the actual PDFs. Access level must match the document.
INSERT INTO document_chunks VALUES
('CH-DEMO-001','DOC001',2,'Refund Eligibility','support'),
('CH-DEMO-002','DOC002',3,'Return Windows','support'),
('CH-DEMO-003','DOC003',4,'Standard Shipping','support'),
('CH-DEMO-004','DOC004',3,'Warranty Periods','support'),
('CH-DEMO-005','DOC005',2,'Cancellation Before Shipment','support'),
('CH-DEMO-006','DOC006',4,'Failed Payments','support'),
('CH-DEMO-007','DOC007',5,'Laptop Specifications','support'),
('CH-DEMO-008','DOC008',5,'Escalation Rules','support'),
('CH-DEMO-009','DOC009',3,'Laptop Overheating','support'),
('CH-DEMO-010','DOC010',1,'Refund Authorization Matrix','admin'),
('CH-DEMO-011','DOC011',1,'Internal Inventory Decision Rules','admin'),
('CH-DEMO-012','DOC012',1,'Compensation Confidentiality','admin');
