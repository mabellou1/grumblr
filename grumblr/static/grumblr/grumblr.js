function populateList() {
    $.get("/grumblr/get-changes")
      .done(function(data) {
          var list = $("#item-list");
          list.data('max-time', data['max-time']);
          list.html('')
          for (var i = 0; i < data.items.length; i++) {
              item = data.items[i];
              var new_item = $(item.html);
              console.log("item id is"+item.id);
              new_item.data("item-id", item.id);
              list.append(new_item);
              $("#cmt-btn-"+item.id).data("item-id", item.id);
              $.get("/grumblr/get-comment/" + item.id)
                .then(function(subdata){
                    var sublist = $("#comment-list-"+subdata.item_id);
                    console.log("this item has comment list "+ subdata.item_id);
                    for(var j = 0;j < subdata.comments.length;j++){
                      comment = subdata.comments[j];
                      var new_comment = $(comment.html);
                      new_comment.data("comment-id", comment.id);
                      sublist.append(new_comment);
                    }
                });
          }
          $(".fo2").on( "click", addComment);

      })
      .fail(function(data){
        console.log(1);
      });

}


function addItem(){
    var itemField = $("#item-field");
    $.post("/grumblr/add-item", {"item": itemField.val()})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}

function addComment(e){
    // var id = $(e.target).parent().data("item.id");
    var id = $(e.target).data("item-id");
    var commentField = $("#comment-field-"+id);
    $.post("/grumblr/add-comment/"+id, {"comment": commentField.val()})
      .done(function(data){
          populateList();
          commentField.val("").focus();
      });
}



function getUpdates() {
    var list = $("#item-list")
    var max_time = list.data("max-time")
    $.get("/grumblr/get-changes/"+ max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              var new_item = $(item.html);
              new_item.data("item-id", item.id);
              list.prepend(new_item);
              $("#cmt-btn-"+item.id).data("item-id", item.id);
              $("#cmt-btn-"+item.id).on( "click", addComment);

          }
      });
}
// dealing with the hustle problem 
$(document).ready(function () {
  // Add event-handlers
  $("#add-btn").click(addItem);
  // $("#cmt-btn").click(addComment);
  // $("#cmt-btn").on("click", "button", addComment);
  // $("#todo-list").click(deleteItem);

  

  // Set up to-do list with initial DB items and DOM data
  populateList(); //get all the objects in the database
  // $("#item-field").focus();
  // $(".fo2").on( "click", function( event ) {
  //   event.preventDefault();
  //   console.log("hi");
  // });


  // Periodically refresh to-do list
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
