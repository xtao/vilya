$ ->
    console.log("DOM is ready")

    # COMPARE
    $(".js-details-target").on "click", ->
        $("div.compare-pr-placeholder").hide()
        $("form.pull-request-composer").show()
