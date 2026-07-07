from pathlib import Path
import pandas as pd


class CarRepository:
    """
    Repository responsible for loading and retrieving
    candidate cars from the dataset.
    """

    def __init__(self):
        self.df = pd.read_csv(Path("data/car_data.csv"))

    def get_candidate_cars(
        self,
        requirements: dict,
        max_candidates: int = 30
    ) -> pd.DataFrame:

        filtered = self.df.copy()

        budget = requirements.get("budget")
        fuel = requirements.get("fuel_type")
        transmission = requirements.get("transmission")
        body_type = requirements.get("body_type")
        family = requirements.get("family_size")

        # ------------------------
        # Budget Filter
        # ------------------------

        if budget:

            lower_limit = budget * 0.80
            upper_limit = budget * 1.10

            filtered = filtered[
                (
                    filtered["Pricing Delhi Ex Showroom Price"] >= lower_limit
                )
                &
                (
                    filtered["Pricing Delhi Ex Showroom Price"] <= upper_limit
                )
            ]

        # ------------------------
        # Fuel Type
        # ------------------------

        if fuel:

            filtered = filtered[
                filtered["Efficiency Fuel Type"]
                .str.lower()
                .str.contains(fuel.lower(), na=False)
            ]

        # ------------------------
        # Transmission
        # ------------------------

        if transmission:

            filtered = filtered[
                filtered["Engine Transmission"]
                .str.lower()
                .str.contains(transmission.lower(), na=False)
            ]

        # ------------------------
        # Body Type
        # ------------------------

        if body_type:

            filtered = filtered[
                filtered["Identification Body Type"]
                .str.lower()
                == body_type.lower()
            ]

        # ------------------------
        # Seating Capacity
        # ------------------------

        if family:

            filtered = filtered[
                filtered["Identification Seating Capacity"] >= family
            ]

        # ------------------------
        # Sort by Budget Proximity
        # ------------------------

        if budget and not filtered.empty:

            filtered = filtered.copy()

            filtered["price_gap"] = (
                filtered["Pricing Delhi Ex Showroom Price"] - budget
            ).abs()

            filtered = (
                filtered
                .sort_values(by="price_gap")
                .drop(columns="price_gap")
            )

        # ------------------------
        # Limit Candidates
        # ------------------------

        return filtered.head(max_candidates)
    
    def get_compact_candidates(self, candidates_df: pd.DataFrame):
        """
        Convert candidate DataFrame into a compact representation
        for the Candidate Selection Agent.
        """

        compact_candidates = []

        for _, car in candidates_df.iterrows():

            compact_candidates.append(
                {
                    "brand": car["Identification Brand"],
                    "model": car["Identification Model"],
                    "variant": car["Identification Variant"],
                    "price": car["Pricing Delhi Ex Showroom Price"],
                    "body_type": car["Identification Body Type"],
                    "fuel_type": car["Efficiency Fuel Type"],
                    "transmission": car["Engine Transmission"],
                    "power_bhp": car["Engine Bhp"],
                    "torque_nm": car["Engine Torque"],
                    "mileage": car["Efficiency Mileage Arai"],
                    "ground_clearance": car["Dimensions Ground Clearance"],
                    "boot_space": car["Dimensions Boot Liters"],
                    "seating_capacity": car["Identification Seating Capacity"],
                    "safety_rating": car["Safety Ncap Stars"]
                }
            )

        return compact_candidates
    
    def get_models(self, selected_models: list):
        """
        Return the full records for the shortlisted models.
        """

        result = []

        for selected in selected_models:

            model_df = self.df[
                (self.df["Identification Brand"] == selected["brand"]) &
                (self.df["Identification Model"] == selected["model"])
            ]

            if not model_df.empty:
                result.extend(model_df.to_dict(orient="records"))

        return result
    
    def get_selected_model_specs(self, selected_models: list):
        """
        Retrieve the complete specifications for the exact
        shortlisted variants.
        """

        model_specs = []

        for selected in selected_models:

            matches = self.df[
                (self.df["Identification Brand"] == selected.brand)
                &
                (self.df["Identification Model"] == selected.model)
                &
                (self.df["Identification Variant"] == selected.variant)
            ]

            if matches.empty:
                continue

            model_specs.append(
                matches.iloc[0].to_dict()
            )

        return model_specs