// JavaScript Document
$(function(){

	$("#codeImg").click(function(e) {
		var src=$(this).attr("src");
		$(this).attr("src",src+"?");
	});

	$(".regForm").ready(function(e) {
		$(this).submit(function(e) {
            var telPhone=$(this).find("input[name='telPhone']");
			if(!(/^1[3|4|5|6|7|8|9][0-9]\d{4,8}$/.test(telPhone.val()))){ 
				alert("请填写真实正确的手机号码！");
				telPhone.focus();
				return false; 
			} 
			
			var password=$(this).find("input[name='password']");
			var pPattern = /^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$/;
			if(!(pPattern.test(password.val()))){ 
				alert("密码由8~16位数字，英文，下划线组成!");
				password.focus();
				return false; 
			}
			
			var password2=$(this).find("input[name='password2']");
			if(!(password2.val()==password.val()))
			{
				alert("两次输入的密码不相同！");
				password2.focus();
				return false; 
			}

			var code=$(this).find("input[name='code']");
			if(code.val()=="")
			{
				alert("请输入手机验证码！");
				code.focus();
				return false; 
			}


			var tk=$(this).find("#tk");
			if(!tk.is(":checked"))
			{
				alert("请阅读并同意服务条款！");
				return false;
			}


        });

		var getCode=$(this).find("a.getCode");
		var sended=false;
		
			getCode.click(function(e) {
				
			if(sended!=false)return;
			
			var telPhone=$("input[name='telPhone']");
			if(!(/^1[3|4|5|6|7|8|9][0-9]\d{4,8}$/.test(telPhone.val()))){ 
				alert("请填写真实正确的手机号码！");
				telPhone.focus();
				return false; 
			}
			
			var vcode=$("input[name='vcode']");
			if(vcode.length==""){ 
				alert("请填写正确的验证码！");
				vcode.focus();
				return false; 
			}
			
			
			sended=true;
			  var url="/sendSms/sendSMScode2.php";
			  $.ajax({url:url,
						  data:{telnum:telPhone.val(),vcode:vcode.val()},
						  type:"post",
						  success: function(result)
						  {
							  if(result=="0")
							  {
								  alert('手机验证码发送成功！');
								  sended=true;
								  var i=60;
								  var t=setInterval(function(){
									  i--;
									  getCode.html("发送成功！"+i+"秒后可重发...");
									  if(i<=0)
									  {
										  clearInterval(t);
										  sended=false;
										  getCode.html("重新发送验证码！");
									  }
									  },1000);
								  
							  }else if(result=="-1")
							  {
								  alert('发送验证码太频繁,请稍候再试！');
								  sended=false;
							  }else if(result=="-2")
							  {
								  alert('验证码不正确！');
								  $("input[name='vcode']").focus();
								  sended=false;
							  }else
							  {
								  alert('手机验证码发送失败！');
								  sended=false;
							  }
						  }
			  });
            });
		
		
    });



});