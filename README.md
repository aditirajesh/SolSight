# OVERVIEW 
SolSight IS an innovative application designed to predict the yield of solar energy panels. This application leverages real-time data and advanced machine learning to provide accurate predictions and maintain the health of solar panels.

## Features 
1. **Data Collection:** SolSight uses the OpenWeatherMap API to fetch real-time information on irradiance and temperature based on the geographical coordinates (latitude and longitude) of the solar panels. This ensures that the predictions are based on the most current weather conditions.

2. **Machine Learning Model:** The core prediction algorithm is powered by XGBoost, a powerful machine learning model known for its accuracy and performance. The model was trained on historical data, encompassing various conditions and scenarios to predict the module temperature. The XGBoost model achieves an impressive accuracy of 98%.

3. **Yield Prediction:** By analyzing the module temperature, ambient temperature, and irradiance, SolSight accurately predicts the energy yield of solar panels. This helps in planning and optimizing energy production.

4. **Panel Health Maintenance:** Beyond yield prediction, SolSight also monitors the health of the solar panels. It provides alerts and mitigation strategies if the panels are found to be working inefficiently, ensuring that the panels operate at their optimal capacity.
