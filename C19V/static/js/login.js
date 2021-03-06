const app = function () {
  const switchButton = document.querySelector(".switch_button");

  const loginBox = document.querySelector(".login");

  const signupBox = document.querySelector(".signupbox");

  const switchText = document.querySelector(".switch_text");

  let toggle = false; //false indicates signup box is hidden

  console.log(switchButton);

  switchButton.addEventListener("click", function () {
    console.log("hello");
    if (!toggle) {
      this.textContent = "Login";
      loginBox.classList.add("sin");
      switchText.textContent = "Already have an account?";
      signupBox.classList.remove("sin");
    } else {
      this.textContent = "Sign up";
      loginBox.classList.remove("sin");
      switchText.textContent = "Create an account?";
      signupBox.classList.add("sin");
    }
    toggle = !toggle;
  });
};
app();
console.log("Script working");
