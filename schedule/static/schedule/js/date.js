$(document).ready(function() {

$("#id_subproject").change(function () {
      var url = $(".project_form").attr("data-artifacts-url");
      var subprojectId = $(this).val();

      $.ajax({
        url: url,
        data: {
          'subproject': subprojectId
        },
        success: function (data) {
          $("#id_artifact").html(data);
        }
      });

    });


$("#id_artifact").change(function () {
    var url = $(".project_form").attr("data-profiles-url");
    var artifactId = $(this).val();

    $.ajax({
        url: url,
        data: {
          'artifact': artifactId
        },
        success: function (data) {
          $("#id_profile").html(data);
    }
    });

});

    $('#id_subproject').select2();
    $('#id_artifact').select2();
    $('#id_profile').select2();


            $("#partial_save").click(function () {
      var date = $(".title").attr("date");
      var project_name = $("#partial_save").attr("data-project-name");
      var url = $(".project_form").attr("data-partial_save-url");
      var subprojectId = $("#id_subproject").val();
      var artifactId = $("#id_artifact").val();
      var profileId = $("#id_profile").val();
      var employeeId = $('input[name="employee"]:checkbox:checked').map(function() {
            return this.value;
        }).get();
      var vehicleId = $('input[name="vehicle"]:checkbox:checked').map(function() {
            return this.value;
        }).get();
      var comment = $("#id_comment").val();




      $.ajax({
        url: url,
        type: "GET",
        data: {
          'date': date,
          'project_name': project_name,
          'subproject': subprojectId,
          'artifact': artifactId,
          'profile': profileId,
          "vehicle": vehicleId,
          "employee": employeeId,
          "comment": comment,
        },
        success: function (data) {
          $("#response_table").html(data);
        }
      });

    });

    var date = $(".title").attr("date");
    var project_name = $("#partial_save").attr("data-project-name");
    var url = $(".project_form").attr("data-partial_save-url");
    var r_type = "first_load";

    $.ajax({
        url: url,
        type: "GET",
        data: {
        'date': date,
        'project_name': project_name,
        "r_type": r_type,
        },
        success: function (data) {
          $("#response_table").html(data);
        }
      });



    $(document).on('click', '.icon', function(){
        var id = $(this).attr("id");
        var r_type = "add or remove"

            $.ajax({
        url: url,
        type: "GET",
        data: {
        'date': date,
        'project_name': project_name,
        "r_type": r_type,
        "id": id
        },
        success: function (data) {
          $("#response_table").html(data);
        }
      });

    });

});