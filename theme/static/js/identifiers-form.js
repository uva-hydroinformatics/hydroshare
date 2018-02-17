function cleanIdentifiers() {
    var identifiers = $(".edit-identifiers-container .well:not(.identifier-template)");

    identifiers.each(function (index, item) {
        if ($(item).find("[name='identifier_link']").val().trim() == "" ||
            $(item).find("[name='identifier_name']").val().trim() == "") {
            $(item).remove();
        }
    });
}

$(document).ready(function () {
    $(".edit-identifiers-container").on("change", ".select-identifier", function () {
        var value = $(this).val();
        var showOther = value === "Other";

        var other = $(this).closest(".well").find(".identifier-specify");

        other.toggleClass("hidden", !showOther);

        if (showOther) {
            other.find("input").attr("name", $(this).attr("name"));
            $(this).removeAttr("name");
        }
        else {
            $(this).attr("name", other.find("input").attr("name"));
            other.find("input").removeAttr("name");
        }
    });

    $(".edit-identifiers-container").on("click", ".close", function () {
        $(this).closest(".well").remove();
    });

    $(".btn-add-identifier").click(function () {
        var templateInstance = $(this).parent().find(".identifier-template").clone();
        templateInstance.toggleClass("hidden", false);
        templateInstance.toggleClass("identifier-template", false);

        templateInstance.find(".select-identifier").attr("name", "identifier_name");
        templateInstance.find(".identifier-link-container input").attr("name", "identifier_link");

        $(this).parent().find(".edit-identifiers-container").append(templateInstance).hide().fadeIn(350);
    });
});