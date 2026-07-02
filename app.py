# =====================================================
# app.py - Script version of the notebook (for Docker/K8s)
# Runs the full pipeline: Load -> EDA -> ETL -> ML
# =====================================================
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, month
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# 1. Start Spark
spark = SparkSession.builder.appName("RetailAnalytics").getOrCreate()

# 2. Load data
df = spark.read.csv("synthetic_transactions.csv", header=True, inferSchema=True)
df.printSchema()
df.show(5)

# 3. Spark SQL analytics
df.createOrReplaceTempView("sales")

print("--- Top 10 Products ---")
spark.sql("""
SELECT product, SUM(quantity) qty FROM sales
GROUP BY product ORDER BY qty DESC LIMIT 10
""").show()

print("--- Category Revenue ---")
spark.sql("""
SELECT category, ROUND(SUM(quantity*price),2) revenue FROM sales
GROUP BY category ORDER BY revenue DESC
""").show()

print("--- Top 5 Customers ---")
spark.sql("""
SELECT customer_id, ROUND(SUM(quantity*price),2) total FROM sales
GROUP BY customer_id ORDER BY total DESC LIMIT 5
""").show()

print("--- Monthly Sales ---")
spark.sql("""
SELECT month(purchase_date) month, ROUND(SUM(quantity*price),2) sales
FROM sales GROUP BY month(purchase_date) ORDER BY month
""").show()

# 4. ETL
clean = df.dropna()
clean = clean.withColumn("amount", col("quantity") * col("price"))
clean.write.mode("overwrite").csv("processed_sales", header=True)
print("ETL complete.")

# 5. ML - Logistic Regression
ml_df = clean.withColumn("label", (col("amount") > 500).cast("int"))
assembler = VectorAssembler(inputCols=["quantity", "price"], outputCol="features")
data = assembler.transform(ml_df).select("features", "label")
train, test = data.randomSplit([0.8, 0.2], seed=42)
model = LogisticRegression().fit(train)
pred = model.transform(test)
acc = MulticlassClassificationEvaluator(metricName="accuracy").evaluate(pred)
print("Model Accuracy:", round(acc, 4))

spark.stop()
print("Pipeline finished successfully.")
