**Energy Toolkit** was initiated in 2024 as a pilot project by [Region Västra Götaland](https://www.vgregion.se/) and [AI Sweden](https://ai.se). The goal of the project is to spread and deepen the understanding of the possibilities for local electricity production and energy self-sufficiency.

## Who Can Use Energy Toolkit

The Energy Toolkit can be used by regional and local stakeholders with an interest in or responsibilities for energy, as well as by industry and the general public. The visual interface is designed to be accessible to anyone with a basic understanding of electricity production.

For more technically inclined users, the underlying power model and scenario generator can be modified. This makes it possible to customize the model and run scenarios that reflect specific conditions in different locations, enabling in-depth analyses and tailored insights.

### User Groups:
1. **Decision Makers** (including the public), who may not have detailed knowledge of the energy sector.
2. **Energy Specialists**, who have deeper expertise in energy issues but may not have detailed knowledge in optimization and power system analysis.
3. **Energy Modelers**, who are experts in modeling power systems.

## What is Energy Toolkit?

The Energy Toolkit consists of four components that can be used independently of each other.

### Component 1: A Framework for Power System Optimization and Analysis

We have built a model for local electricity production and storage from various energy sources. This model serves as the foundation for the rest of the system. We use [PyPSA](https://pypsa.org/) in this component, a powerful tool for simulating and optimizing power systems.

**_How this component can be used_**
- **Decision Makers** use this component only through other components.
- **Energy Specialists** use this component only through other components.
- **Energy Modelers** can modify the energy model, add or remove energy sources or storage forms, and set additional constraints on the system. These changes can then be run individually or through the data generator.

### Component 2: A Data Generator

The data generator is used to run a large number of scenarios through our model. We can pre-generate the data that is analyzed in later stages in an efficient manner. The production model can also be partly controlled by changing the scenario parameters.

**_How this component can be used_**
- **Decision Makers** use this component only through other components.
- **Energy Specialists** can change scenario parameters to better adapt them to local conditions or look at specific, particularly relevant scenarios.
- **Energy Modelers** can run new models through the data generator and edit input data for models similarly to energy specialists.

### Component 3: An API

Output from the generator is stored in an API, making the data accessible for analysis in any software and with any methods.

**_How this component can be used_**
- **Decision Makers** use this component only through other components.
- **Energy Specialists** can change scenario parameters to better adapt them to local conditions or look at specific, particularly relevant scenarios.
- **Energy Modelers** can run new models through the data generator and edit input data for models similarly to energy specialists.

### Component 4: An App

To visualize the results, we have built our own Streamlit-based app. Through this app, we provide all user groups with an intuitive interface to explore and experiment with the model.

**_How this component can be used_**
- **Decision Makers** can use the app to deepen their understanding, as a basis for meetings with experts and stakeholders, or in dialogue with the public.
- **Energy Specialists** can use the app to communicate more effectively in their operations.
- **Energy Modelers** can use the app to validate and test new models.

## Usage

The Energy Toolkit can be used by regional and local stakeholders with an interest in or responsibilities for energy, as well as by industry and the general public. The visual interface is designed to be broadly accessible, catering to anyone with a basic understanding of electricity generation.

For more technically inclined users, the underlying power model and scenario generator can be modified. This allows for the customization of the model and the execution of scenarios that reflect the specific conditions of different localities, enabling in-depth analysis and tailored insights.
