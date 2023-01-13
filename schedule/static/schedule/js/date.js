$(document).ready(function() {
  // Select the forms using their class attribute
  var forms = $('.js_form[data-hassubproject="True"]');


  forms.each(function(index) {
    // Update the id attribute of the subproject element
    $(this).find('[name="subproject"]').attr("id", $(this).find('[name="subproject"]').attr("id") + index);
    // Update the id attribute of the artifact element
    $(this).find('[name="artifact"]').attr("id", $(this).find('[name="artifact"]').attr("id") + index);
    // Update the id attribute of the profile element
    $(this).find('[name="profile"]').attr("id", $(this).find('[name="profile"]').attr("id") + index);
    // Update the id attribute of the comment element
    $(this).find('[name="comment"]').attr("id", $(this).find('[name="comment"]').attr("id") + index);
    // Update the id attribute of the response_table element
    $(this).find('#response_table').attr("id", $(this).find('#response_table').attr("id") + index);
    });
   });

$(document).ready(function() {
  $('.select2').each(function() {
    $(this).select2();
  });
});

$(document).ready(function() {
  // Select the forms using their class attribute
  var forms = $('.js_form[data-hassubproject="True"]');



  // Set up event listeners for the form elements
  forms.each(function() {
    // Select the form elements using the name attribute of the form
    var subproject = $(this).find('[name="subproject"]');
    var artifact = $(this).find('[name="artifact"]');
    var profile = $(this).find('[name="profile"]');
    var employee = $(this).find('input[name="employee"]');
    var vehicle = $(this).find('input[name="vehicle"]');
    var comment = $(this).find('[name="comment"]');
    var partialSaveButton = $(this).closest('.project').find('[name="update"]');
    var response_table = $(this).closest('.project').find('[id^="response_table"]');


    // Set up event listeners for changes in the subproject element
    subproject.change(function () {
      var url = $(this).closest('.js_form').data('artifacts-url');
      var subprojectId = $(this).val();

      $.ajax({
        url: url,
        data: {
          'subproject': subprojectId
        },
        success: function (data) {
          artifact.html(data);
        }
      });
    });

    // Set up event listeners for changes in the artifact element
    artifact.change(function () {
      var url = $(this).closest('.js_form').data('profiles-url');
      var artifactId = $(this).val();

      $.ajax({
        url: url,
        data: {
          'artifact': artifactId
        },
        success: function (data) {
          profile.html(data);
        }
      });
    });

    // Set up event listeners for clicks on elements with the 'icon' class
    $(this).on('click', '.icon', function(){
    console.log($(this))
      var project_id = $(this).closest(".js_form").find("[name='project_id']").val();
      var id = $(this).attr("id");
      var r_type = "add or remove";
      var url = $(this).closest('.js_form').data('partial_save-url');
      var date = $(".title").attr("date");
      var project_name = partialSaveButton.data("project-name");

      $.ajax({
        url: url,
        type: "GET",
        data: {
          'date': date,
          'project_name': project_name,
          "r_type": r_type,
          "id": id,
          'project_id': project_id,
        },
        success: function (data) {
          response_table.html(data);
        }
      });
    });

   // Set up event listeners for clicks on the partial save(update) button
partialSaveButton.click(function () {
  var date = $(".title").attr("date");
  var project_name = partialSaveButton.data("project-name");
  var project_id = $(this).closest(".project").find("[name='project_id']").val();
  var url = $(this).closest('.project').find('.js_form').data('partial_save-url');
  console.log(url);
  var subprojectId = subproject.val();
  var artifactId = artifact.val();
  var profileId = profile.val();
  var employeeId = $(this).closest('.project').find('input[name="employee"]:checkbox:checked').map(function() {
            return this.value;
        }).get();
  var vehicleId = $(this).closest('.project').find('input[name="vehicle"]:checkbox:checked').map(function() {
            return this.value;
        }).get();
  var comment_ = comment.val();

  $.ajax({
    url: url,
    type: "GET",
    data: {
      'date': date,
      'project_name': project_name,
      'project_id': project_id,
      'subproject': subprojectId,
      'artifact': artifactId,
      'profile': profileId,
      "vehicle": vehicleId,
      "employee": employeeId,
      "comment": comment_,
    },
    success: function (data) {
      response_table.html(data);
    }
  });
});

// Load the initial data for the form
if (partialSaveButton.data("project-name")) {
  var url = $(this).closest('.js_form').data('partial_save-url');
  var project_name = partialSaveButton.data("project-name");
  var project_id = $(this).find("[name='project_id']").val();

  console.log(url)

  $.ajax({
    url: url,
    type: "GET",
    data: {
      'project_name': project_name,
      'project_id': project_id,
    },
    success: function (data) {
      response_table.html(data);
      console.log(response_table)
    }
  });
}
});
});





