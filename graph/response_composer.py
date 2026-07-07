def response_composer(state):

    return {

        "consultation_report": {

            "recommendation": state["recommendation"],

            "purchase_advisory": state["purchase_advisory"]

        },

        "execution_log": [
            {
                "node": "Response Composer",
                "message": "Generated consultation report."
            }
        ]
    }