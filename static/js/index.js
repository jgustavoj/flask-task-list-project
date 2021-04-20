$(document).ready(function () {
  $(".up").on("click", function (e) {
    var wrapper = $(this).closest("li");
    wrapper.insertBefore(wrapper.prev());
  });
  $(".down").on("click", function (e) {
    var wrapper = $(this).closest("li");
    wrapper.insertAfter(wrapper.next());
  });
});
