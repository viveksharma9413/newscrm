
        function ValidateEmail(mail)
        {
            var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
            if(mail.value.match(mailformat))
            {
                document.loginForm.email.focus();
                return true;
            }

            else
            {
                alert("You have entered an invalid email address!");
                document.subscribeForm.email.focus();
                return false;
            }
        }

        function ValidatePhn(phn)
        {
            var phnformat = /^[789]\d{9}$/;
            if(phn.value.match(phnformat))
            {
                document.subscribeForm.phnNo.focus();
                return true;
            }

            else
            {
                alert("You have entered an invalid phnNo!");
                document.subscribeForm.phnNo.focus();
                return false;
            }
        }

        function ValidateName(name)
        {
            if(name.length==0)
            {
                alert("You have entered an invalid Name!");
                document.subscribeForm.name.focus();
                return false;
            }
        }

        function Validate(email,phn,name)
        {
            ValidateName(name);
            ValidateEmail(email);
            ValidatePhn(phn);
        }

        function Validate2(email,phn)
        {
            ValidateEmail(email);
            ValidatePhn(phn);
        }