// page init
jQuery(function(){
"use strict";
	FixedHeader();
	ImageFitCont();
});

// Fixed Header
function FixedHeader() {
	var lastScrollTop = 0, delta = 5;

	if ($(window).width() > 1024) {
		$(window).scroll(function(event){
		   var st = $(this).scrollTop();

		   if(Math.abs(lastScrollTop - st) <= delta)
			  return;

		   if (st > lastScrollTop){
		   // downscroll code
		   $(".admin-header").addClass('in-fix-head').css({top:'-65px'});
		   $("body").addClass('slim-header');
		   //.hover(function(){$(".admin-header").removeClass('in-fix-head').css({top: '0px'})})
		   } else {
			  // upscroll code
			  $(".admin-header").removeClass('in-fix-head').css({top:'0px'});
			  $("body").removeClass('slim-header');
		   }
		   lastScrollTop = st;
		});
	}
	else {
		$(window).scroll(function(event){
		   var st = $(this).scrollTop();

		   if(Math.abs(lastScrollTop - st) <= delta)
			  return;

		   if (st > lastScrollTop){
		   // downscroll code
		   $(".site-inner-header").addClass('in-fix-head').css({top:'-130px'});

		   }
		   if (st < 50){
		   // downscroll code
		   $(".site-inner-header").removeClass('in-fix-head').css({top:'0px'});

		   } else {
			  // upscroll code
			  //$(".site-inner-header").removeClass('in-fix-head').css({top:'0px'});
		   }
		   lastScrollTop = st;
		});
	}
}


// Image Fit Container
function ImageFitCont() {
	"use strict";
	$('.imageFit').imgLiquid({
		fill: true,
        horizontalAlign: 'center',
        verticalAlign: 'center'
	});
}


$( function() {
	"use strict";

	// Left Nav Toggle
	$(document).on('click', '.nav-toggle', function(e) {
		e.preventDefault();
		$('body').toggleClass('visible-nav');
	});

	/////////// Custom Scrollbar
	setTimeout(function(){
		$(".left-panel").mCustomScrollbar({
			theme:"dark-thin",
			scrollbarPosition:"outside"
		});
		
		
	}, 1000);

	///////// Footer Shown
	$(window).scroll(function() {
	   if($(window).scrollTop() + $(window).height() == $(document).height()) {
		   //alert("bottom!");
		   $('body').addClass('footer-shown');
		   $('.admin-footer').addClass('foot-visile');
	   }
	   else{
		   $('body').removeClass('footer-shown');
		   $('.admin-footer').removeClass('foot-visile');
	   }
	});

	//////////// Left Menu Active
	$('#accordion .panel').on('show.bs.collapse hide.bs.collapse', function(e) {
		if (e.type=='show'){
		  $(this).addClass('activestate');
		}else{
		  $(this).removeClass('activestate');
		}
	});


	///////// Clear Search Field
	$('.cs').clearSearch();

	
	
	///////Header Date Toggle
	if ($(window).width() < 1400) {
		$(document).on('click', function(e) {
			var elem = $(e.target).closest('#BtnDate'),
				box  = $(e.target).closest('#dateWrap');
			
			if ( elem.length ) {
				e.preventDefault();
				$('#dateWrap').toggle();
			}else if (!box.length){
				$('#dateWrap').hide();
			}
		});
		
	}
	
	if ($(window).width() < 1024) {
		// Mobile Doc Toolbar
		$(document).on('click', '.toggle-doc', function() {
			$(this).toggleClass('doc-close');
			$('.header-bottom .doc-toolbar-cont').fadeToggle();
		});
		
		// Mobile Doc Toolbar
		$(document).on('click', '.close-leftmenu', function() {
			$('body').removeClass('visible-nav');
		});
	}
	
	/*setTimeout(function(){
		$('#my-table').tablesorter();
	},4000);*/
	
	/*$('#ListView').on('shown.bs.modal', function() {
		alert();
	});*/
	
	

});





// $(window).on('load', function(e) {
// 	setTimeout(function(){
// 		$('.count').each(function () {
// 			$(this).prop('Counter',0).animate({
// 				Counter: $(this).text()
// 			}, {
// 				duration: 3000,
// 				easing: 'swing',
// 				step: function (now) {
// 					$(this).text(Math.ceil(now));
// 				}
// 			});
// 		});
// 	},4000);
// });
