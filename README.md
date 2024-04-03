**Agriculture Land Use Analysis in Arizona**

This project delves into the intricate patterns of agricultural land use, aiming to provide comprehensive insights into cultivation practices, irrigation requirements, and socio-economic implications. Our approach combines advanced data analysis techniques with predictive modeling to offer valuable information for policymakers, researchers, and agricultural stakeholders.

**Objectives**

The primary objectives of this project are:
- Analyze agriculture land use patterns in Arizona.
- Identify irrigation requirements and best crops based on terrain information.
- Predict regions of similar terrain suitable for agriculture.
- Understand concerns in migrations to other regions.
- Provide data-driven insights into agriculture land use and irrigation patterns to policymakers.

**Datasets Used**

We utilized a diverse range of datasets to achieve our objectives, including:
- USDA NASS Cropland Data Layers
- SRTM Digital Elevation Data Version 4
- Daymet V4: Daily Surface Weather and Climatological Summaries
- GFSAD1000: Cropland Extent 1km Multi-Study Crop Mask, Global Food-Support Analysis Data
- GRIDMET DROUGHT: CONUS Drought Indices

**Approach**

Our approach involved a series of comprehensive analyses and modeling techniques:
- Collected precipitation, maximum temperature, minimum temperature, and drought data from Google Earth Engine spanning the past 15 years.
- Performed linear regression analysis to identify trends and predict values for precipitation, temperature, and drought conditions for the next 5 years.
- Trained an XGBoost model for crop and irrigation level prediction based on temperature and precipitation data, achieving an accuracy rate of 89%.
- Utilized DBSCAN for clustering agricultural lands, uncovering significant occupancy by Native American tribes.
- Proposed an innovative application that utilizes environmental features to suggest optimal crop choices and irrigation levels based on user-provided location data.

**Recognition**

This project received an honorary mention in the SpaceHACK For Sustainability hackathon for its innovative approach and contributions to sustainable agriculture.

**UN Sustainable Development Goals (SDGs)**

Our project aligns with several UN SDGs, including:
- Goal 12: Responsible Consumption and Production
- Goal 2: Zero Hunger
- Goal 8: Decent Work and Economic Growth
- Goal 13: Climate Action

**Resources and References**

We acknowledge the valuable resources and references that contributed to our project, including various datasets and the Native Peoples of Arizona Map.

This README provides an overview of our project's objectives, approach, datasets used, and alignment with UN SDGs. For further details, refer to the project's documentation and codebase. Thank you for your interest in our Agriculture Land Use Analysis in Arizona project!
