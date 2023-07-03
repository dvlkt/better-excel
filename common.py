ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

EXAMPLE_DATA = {
    1: {
        "width": 7,
        "height": 3,
        "content": [
            {
                "error_col": False,
                "content": [{
                    "value": "l1 (m)",
                    "parsed_value": "l1 (m)",
                    "has_error": False
                },
                {
                    "value": "0.264",
                    "parsed_value": "0.264",
                    "has_error": False
                },
                {
                    "value": "",
                    "parsed_value": "",
                    "has_error": False
                },
                {
                    "value": "",
                    "parsed_value": "",
                    "has_error": False
                }]
            },
            {
                "error_col": False,
                "content": [{
                    "value": "l2 (m)",
                    "parsed_value": "l2 (m)",
                    "has_error": False
                },
                {
                    "value": "0.28",
                    "parsed_value": "0.28",
                    "has_error": False
                },
                {
                    "value": "0.33",
                    "parsed_value": "0.33",
                    "has_error": False
                },
                {
                    "value": "0.383",
                    "parsed_value": "0.383",
                    "has_error": False
                }]
            },
            {
                "error_col": False,
                "content": [{
                    "value": "t (s)",
                    "parsed_value": "t (s)",
                    "has_error": False
                },
                {
                    "value": "3.53",
                    "parsed_value": "3.53",
                    "has_error": False
                },
                {
                    "value": "6.21",
                    "parsed_value": "6.21",
                    "has_error": False
                },
                {
                    "value": "7.3",
                    "parsed_value": "7.3",
                    "has_error": False
                }]
            },
            {
                "error_col": False,
                "content": [{
                    "value": "N",
                    "parsed_value": "N",
                    "has_error": False
                },
                {
                    "value": "10",
                    "parsed_value": "10",
                    "has_error": False
                },
                {
                    "value": "10",
                    "parsed_value": "10",
                    "has_error": False
                },
                {
                    "value": "10",
                    "parsed_value": "10",
                    "has_error": False
                }]
            },
            {
                "error_col": False,
                "content": [{
                    "value": "T (s)",
                    "parsed_value": "T (s)",
                    "has_error": False
                },
                {
                    "value": "0.353",
                    "parsed_value": "0.353",
                    "has_error": False
                },
                {
                    "value": "0.621",
                    "parsed_value": "0.621",
                    "has_error": False
                },
                {
                    "value": "0.73",
                    "parsed_value": "0.73",
                    "has_error": False
                }]
            },
            {
                "error_col": False,
                "content": [{
                    "value": "&delta;t (s)",
                    "parsed_value": "δt (s)",
                    "has_error": False
                },
                {
                    "value": "=!1B1-!1A$1",
                    "parsed_value": "0.016",
                    "has_error": False
                },
                {
                    "value": "=!1B2-!1A$1",
                    "parsed_value": "0.066",
                    "has_error": False
                },
                {
                    "value": "=!1B3-!1A$1",
                    "parsed_value": "0.119",
                    "has_error": False
                }]
            },
            {
                "error_col": False,
                "content": [{
                    "value": "g (m/s^2)",
                    "parsed_value": "g (m/s^2)",
                    "has_error": False
                },
                {
                    "value": "=((2*$PI)^2 * !1F1) / !1E1^2",
                    "parsed_value": "5.0690935781",
                    "has_error": False
                },
                {
                    "value": "=((2*$PI)^2 * !1F2) / !1E2^2",
                    "parsed_value": "6.7564796323",
                    "has_error": False
                },
                {
                    "value": "=((2*$PI)^2 * !1F3) / !1E3^2",
                    "parsed_value": "8.8157847531",
                    "has_error": False
                }]
            }
        ]
    }
}

table_data = {} # EXAMPLE_DATA