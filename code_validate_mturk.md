```javascript
<script src="https://assets.crowd.aws/crowd-html-elements.js"></script>
<div id="errorBox"></div>
<crowd-form>
    <label for="surveycode">Provide the code here: </label>
    <crowd-input id="surveycode" name="surveycode">
    </crowd-input>
    <button id='check'>Check your code</button>
</crowd-form>
<script>
	$(document).ready(function() {
		$('#check').click(async function(e) {
		    e.preventDefault();
	        let user_input = document.getElementById('surveycode').value;
		    await fetch("https://yourbackend?input=" + user_input)
		    .then(response => response.json())
		    .then(data => {
                // code validation failed
		        if (data['status'] == 'failed') {
		            errorBox.innerHTML = '<crowd-alert type="error" dismissible>You must provide a valid code.</crowd-alert>';
                    errorBox.scrollIntoView();
                // good code and submit the HIT
		        } else {
		            document.querySelector('crowd-form').submit();
		        }
		    })
	    })
	})
</script>
