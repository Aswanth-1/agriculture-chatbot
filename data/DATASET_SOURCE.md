# Dataset Source

This folder uses a public Crop Recommendation dataset for the chatbot's crop and fertilizer responses.

Source used for the CSV file:
https://github.com/nileshiq/Crop-Recommendation/blob/main/Crop_Recommendation.csv

Original Kaggle dataset page referenced by the source repository:
https://www.kaggle.com/datasets/varshitanalluri/crop-recommendation-dataset/data

The dataset contains 2,200 rows and these columns:

- Nitrogen
- Phosphorus
- Potassium
- Temperature
- Humidity
- pH_Value
- Rainfall
- Crop

The chatbot summarizes this dataset by crop and uses the average N, P, K values plus the observed temperature, humidity, pH, and rainfall ranges to answer crop-related questions.
