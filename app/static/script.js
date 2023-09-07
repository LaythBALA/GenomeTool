$(document).ready(function(){
	scrollToBottom();
	function scrollToBottom() {
		var commentsList = $(".comments");
		commentsList.animate({
			scrollTop: commentsList.prop("scrollHeight")
		}, 500); // Adjust the animation duration as needed
	}
	$(document).on("submit","#comment-form",function(e){
		e.preventDefault();
		$("#submit-comment").trigger(click);
	})
	$(document).on("click","#submit-comment",function(e){
		var commentText = $("#comment-text").val();
		var position = $("#position").val();
        var thiss=$(this);
		
        // Check if the comment is not empty
        if (commentText.trim() !== "") {
			thiss.prop("disabled",true);
            // Send an AJAX POST request to submit the comment
            $.ajax({
                type: "POST",
                url: "/submit_comment",
                data: {
                    comment: commentText,
                    position: position // Pass the current position
                },
                success: function(response) {
                    // Assuming the response is a JSON object with the new comment
                    var newComment = response.comment;
                    
                    // Add the new comment to the comments list
                    $(".comments ul").append('<li><div class="media"><div class="media-body"><h5 class="mt-0">'+ newComment.user.username +'</h5>'+ newComment.comment +'</div></div></li>');
                    
                    // Clear the comment input field
                    $("#comment-text").val("");
					thiss.prop("disabled", false);
					scrollToBottom();
                }
            });
        }
		
	})
	$(document).on("click",".upload button",function(e){
		$(this).parent().find("input").trigger("click")
	});
	$(document).on("change", ".upload input", function(e) {
		var uploadedFile = e.target.files[0];
		if (!uploadedFile) {
			return;
		}

		var reader = new FileReader();
		reader.onload = function(e) {
			var fileContent = e.target.result;
			
			var position=containsIframeWithPositionParameter(fileContent)
			if (position!==false) {
				window.location="/annotation/"+position;
			} else {
				alert("The uploaded HTML file does not contain the required iframe.");
			}
		};
		reader.readAsText(uploadedFile);
	});
	$(document).on("click",".download button",function(e){
		var annotationPage = $(this).closest('.annotation-page');
		var iframe = annotationPage.find('.annotation-iframe');
		// Check if the iframe exists
		if (iframe.length > 0) {
			var iframe_url=iframe.attr("src")
			console.log(iframe_url)
			var iframeContent =  '<iframe src="'+iframe_url+'" width="800" height="600" frameborder="0" class="annotation-iframe"></iframe>';
			
			// Create a Blob object with the iframe content
			var blob = new Blob([iframeContent], { type: 'text/html' });
			
			// Create a temporary <a> element to trigger the download
			// window.location.href=URL.createObjectURL(blob);
			var a = $('<a>', {
				href: URL.createObjectURL(blob),
				class:"download-iframe",
				download: 'iframe_'+getPositionParameterValue(iframe_url)+'.html',
				style: 'display: none;'
			});
			$('body').append(a);
			a[0].click();
			a.remove();
		} else {
			alert('No iframe found.');
		}
	})
	function getPositionParameterValue(url) {
		var match = url.match(/position=([^&]+)/);
		if (match) {
			return match[1];
		}
		return false; // Return null if the parameter is not found
	}
	function containsIframeWithPositionParameter(htmlContent) {
		var $tempDiv = $('<div>');
		$tempDiv.html(htmlContent);

		var iframe = $tempDiv.find('.annotation-iframe');

		if(iframe.length>0){
			// console.log(iframe.attr("src"));
			return getPositionParameterValue(iframe.attr("src"));
		}

		return false;
	}
})