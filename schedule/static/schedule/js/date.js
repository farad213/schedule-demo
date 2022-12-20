$("#id_subproject").change(function () {
      var url = $(".project_form").attr("data-artifacts-url");  // get the url of the `load_cities` view
      var subprojectId = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'subproject': subprojectId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#id_artifact").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });

    });


        $("#id_artifact").change(function () {
      var url = $(".project_form").attr("data-profiles-url");  // get the url of the `load_cities` view
      var artifactId = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'artifact': artifactId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#id_profile").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });

    });



$(document).ready(function() {
            $("#partial_save").click(function () {
      var date = $(".title").attr("date");
      var project_name = $("#partial_save").attr("data-project-name");
      var url = $(".project_form").attr("data-partial_save-url");
      var subprojectId = $("#id_subproject").val();
      var artifactId = $("#id_artifact").val();
      var profileId = $("#id_profile").val();

      $.ajax({
        url: url,
        type: "GET",
        data: {
          'date': date,
          'project_name': project_name,
          'subproject': subprojectId,
          'artifact': artifactId,
          'profile': profileId,
        },
        success: function (data) {
          $("#response").html(data);
        }
      });

    });
    });

$(document).ready(function() {
    $('#id_subproject').select2();
    $('#id_artifact').select2();
    $('#id_profile').select2();
});