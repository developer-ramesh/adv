jQuery(function(){

  jQuery('#frm_login').submit(function(){
    var ret=true;
      $(this).find('.chk').each(function(){
        if ($(this).val()=='') {
          $(this).addClass('err');
          $(this).parent().find('.err_msg').remove();
          $(this).after('<span class="err_msg" style="color:#FF001F;">This field is required.</span>');
          ret=false;
        }else{
          $(this).next().html('');
          $(this).removeClass('err');
        }
      });
      if(ret==true){
        jQuery('.loader').show();
        jQuery('.btn-success').val('Please wait...');
      }
    return ret;
  });


  jQuery('#frm_reset_pass').submit(function(){
    var ret=true;
      $(this).find('.chk').each(function(){
        if ($(this).val()=='') {
          $(this).addClass('err');
          $(this).parent().find('.err_msg').remove();
          $(this).after('<span class="err_msg" style="color:#FF001F;">This field is required.</span>');
          ret=false;
        }else{
          $(this).next().html('');
          $(this).removeClass('err');
        }
      });

      if(ret==true){
        if($('#new_password').val()!=$('#re_password').val())
        {
          $('#re_password').parent().find('.err_msg').remove();
          $('#re_password').after('<span class="err_msg" style="color:#FF001F;">New Password and Confirm Password must be same.</span>');
          $('#re_password').addClass('err');
          ret=false;
        }
      }
      if(ret==true){
        if($('#result').attr('class')=='short'){
          $('#new_password').addClass('err');
          ret=false;
        }
      }

      if(ret==true){
        jQuery('.loader').show();
        jQuery('.btn-success').val('Please wait...');
      }
    return ret;
  });



$('#new_password').keyup(function() {
$('#result').html( checkStrength($('#new_password').val()) )
});

function checkStrength(password)
{
    var strength = 0
    if (password.length < 1) {
    $('#result').removeClass()
    $('#result').addClass('')
    return ''
    }
    if (password.length < 6) {
    $('#result').removeClass()
    $('#result').addClass('short')
    return 'Too short'
    }
    if (password.length > 7) strength += 1
    // If password contains both lower and uppercase characters, increase strength value.
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
    // If it has numbers and characters, increase strength value.
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
    // If it has one special character, increase strength value.
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    // If it has two special characters, increase strength value.
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    // Calculated strength value, we can return messages
    // If value is less than 2

    if (strength < 2) {
    $('#result').removeClass()
    $('#result').addClass('weak')
    return 'Weak'
    } else if (strength == 2) {
    $('#result').removeClass()
    $('#result').addClass('good')
    return 'Good'
    } else {
    $('#result').removeClass()
    $('#result').addClass('strong')
    return 'Strong'
    }
}



});
