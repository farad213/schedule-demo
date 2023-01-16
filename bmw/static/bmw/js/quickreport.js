$(document).ready(function() {

    // Add event listener to the building select
    $("#id_building").on("change", function() {
        if ($(this).val() === "Other") {
            // Insert new input field for custom building after the building field
            $("#id_building").after(`
                <input type="text" id="id_custom_building" name="custom_building" placeholder="Other">
            `);
        } else {
            // Remove the custom building input field
            $("#id_custom_building").remove();
            $("#id_custom_building_label").remove();
        }
    });

     // Add event listener to the add_profile button
    $("#add_profile").on("click", function() {
         $(this).before(`
            <div class="profiles">
                <input type="number" class="profile_from" name="profile_from"> - <input type="number" class="profile_to" name="profile_to">
            </div>
        `);
    });
});