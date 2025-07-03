{
  "metadata": {
    "course": {
      "name": "Calculo 3",
      "subject_area": "calculo",
      "level": 3
    },
    "assignment": {
      "type": "TAREA",
      "number": 18,
      "year": 2025,
      "month": 6,
      "iteration": 1
    },
    "file_info": {
      "base_name": "C3_2025_T18_integrales_v1",
      "source_file": "C3_2025_T18_3_integrales.json",
      "generated_date": "2025-06-27",
      "processed_date": null,
      "version": "1.0"
    },
    "output_settings": {
      "units": "u",
      "decimal_precision": 4,
      "show_steps": false,
      "equation_format": {
        "show_quantity_label": true,
        "show_equation": true
      }
    },
    "processing_info": {
      "total_exercises": 3,
      "individual_exercises": 2,
      "grouped_exercises": 1,
      "exercise_types": ["integral"],
      "processing_time": null,
      "errors": []
    }
  },
  "exercises": [
    {
      "id": "1",
      "id_letter": null,
      "id_part": null,
      "type": "integral",
      "function": "x**2 + 3*y**2",
      "integrals": [
        { "var": "y", "limits": { "lower": "1", "upper": "2" }, "order": 1 },
        { "var": "x", "limits": { "lower": "0", "upper": "2" }, "order": 2 }
      ],
      "coordinate_system": "cartesian",
      "solution": {
        "exact": "50/3",
        "decimal": 16.6667,
        "quantity_type": null,
        "units": null
      },
      "latex": {
        "integral_setup": null,
        "solution_steps": null,
        "final_result": null
      },
      "computation_details": {
        "intermediate_steps": null,
        "substitutions": null,
        "integration_method": null
      },
      "display_settings": {
        "show_quantity_label": true,
        "show_equation": true,
        "show_steps": false,
        "units": "u",
        "decimal_precision": 4
      }
    },
    {
      "id": "4",
      "id_letter": null,
      "id_part": 1,
      "type": "integral",
      "function": "2*r",
      "integrals": [
        { "var": "r", "limits": { "lower": "0", "upper": "5*sin(theta)" }, "order": 1 },
        { "var": "theta", "limits": { "lower": "0", "upper": "pi/6" }, "order": 2 }
      ],
      "coordinate_system": "polar",
      "solution": {
        "exact": null,
        "decimal": null,
        "quantity_type": null,
        "units": null
      },
      "latex": {
        "integral_setup": null,
        "solution_steps": null,
        "final_result": null
      },
      "computation_details": {
        "intermediate_steps": null,
        "substitutions": null,
        "integration_method": null
      },
      "display_settings": {
        "show_quantity_label": true,
        "show_equation": true,
        "show_steps": false,
        "units": "u",
        "decimal_precision": 4
      }
    },
    {
      "id": "4",
      "id_letter": null,
      "id_part": 2,
      "type": "integral",
      "function": "3*r^2",
      "integrals": [
        { "var": "r", "limits": { "lower": "0", "upper": "2*cos(theta)" }, "order": 1 },
        { "var": "theta", "limits": { "lower": "0", "upper": "pi/4" }, "order": 2 }
      ],
      "coordinate_system": "polar",
      "solution": {
        "exact": null,
        "decimal": null,
        "quantity_type": null,
        "units": null
      },
      "latex": {
        "integral_setup": null,
        "solution_steps": null,
        "final_result": null
      },
      "computation_details": {
        "intermediate_steps": null,
        "substitutions": null,
        "integration_method": null
      },
      "display_settings": {
        "show_quantity_label": true,
        "show_equation": true,
        "show_steps": false,
        "units": "u",
        "decimal_precision": 4
      }
    }
  ]
}