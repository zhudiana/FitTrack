import { useState } from "react";
import bgImage from "../assets/bg_image.png";
import { loginUser, saveToken } from "../api";

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (isLogin) {
      try {
        const data = await loginUser(formData.username, formData.password);
        saveToken(data.access_token);
        console.log("Login successful");
      } catch (error) {
        console.error("Login failed:", error);
      }
    }
  };

  const handleGoogleSignIn = () => {
    // Will be integrated with backend later
    console.log("Google sign-in clicked");
  };

  return (
    <div
      className="h-screen w-screen flex items-center justify-center md:justify-start relative p-5 md:pl-[20px] box-border overflow-hidden"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      {/* Gradient Overlay */}
      <div
        className="absolute inset-0 z-0"
        style={{
          background:
            "linear-gradient(135deg, rgba(102, 126, 234, 0.75) 0%, rgba(118, 75, 162, 0.75) 100%)",
        }}
      ></div>

      {/* Login Card */}
      <div className="relative z-10 bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-6 md:p-12 w-full max-w-[550px] animate-slide-up mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-[42px] font-bold bg-gradient-primary bg-clip-text text-transparent mb-2 tracking-tight">
            FitTrack
          </h1>
          <p className="text-gray-500 dark:text-gray-400 text-base m-0 font-normal">
            Track your progress, achieve your goals
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 bg-gray-100 dark:bg-gray-700 p-1 rounded-xl">
          <button
            className={`flex-1 py-3 px-6 border-none bg-transparent text-gray-500 dark:text-gray-400 text-[15px] font-semibold cursor-pointer rounded-lg transition-all duration-200 ${
              isLogin
                ? "bg-white dark:bg-gray-600 text-primary-purple shadow-sm"
                : "hover:text-primary-purple"
            }`}
            onClick={() => setIsLogin(true)}
          >
            Sign In
          </button>
          <button
            className={`flex-1 py-3 px-6 border-none bg-transparent text-gray-500 dark:text-gray-400 text-[15px] font-semibold cursor-pointer rounded-lg transition-all duration-200 ${
              !isLogin
                ? "bg-white dark:bg-gray-600 text-primary-purple shadow-sm"
                : "hover:text-primary-purple"
            }`}
            onClick={() => setIsLogin(false)}
          >
            Create Account
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-5 mb-6">
          {!isLogin && (
            <div className="flex flex-col gap-2">
              <label
                htmlFor="username"
                className="text-sm font-semibold text-gray-700 dark:text-gray-200"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter your username"
                required={!isLogin}
                className="py-3.5 px-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl text-[15px] transition-all duration-200 font-inherit bg-gray-50 dark:bg-gray-700 dark:text-gray-200 placeholder-gray-400 focus:outline-none focus:border-primary-purple focus:bg-white dark:focus:bg-gray-600 focus:ring-4 focus:ring-primary-purple/10"
              />
            </div>
          )}

          <div className="flex flex-col gap-2">
            <label
              htmlFor="email"
              className="text-sm font-semibold text-gray-700 dark:text-gray-200"
            >
              Email or username
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email or username"
              required
              className="py-3.5 px-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl text-[15px] transition-all duration-200 font-inherit bg-gray-50 dark:bg-gray-700 dark:text-gray-200 placeholder-gray-400 focus:outline-none focus:border-primary-purple focus:bg-white dark:focus:bg-gray-600 focus:ring-3 focus:ring-primary-purple/10"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="password"
              className="text-sm font-semibold text-gray-700 dark:text-gray-200"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              className="py-3.5 px-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl text-[15px] transition-all duration-200 font-inherit bg-gray-50 dark:bg-gray-700 dark:text-gray-200 placeholder-gray-400 focus:outline-none focus:border-primary-purple focus:bg-white dark:focus:bg-gray-600 focus:ring-3 focus:ring-primary-purple/10"
            />
          </div>

          <button
            type="submit"
            className="py-4 bg-gradient-primary text-white border-none rounded-xl text-base font-semibold cursor-pointer transition-all duration-200 mt-2 shadow-lg shadow-primary-purple/40 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-primary-purple/50 active:translate-y-0"
          >
            {isLogin ? "Sign In" : "Create Account"}
          </button>
        </form>

        {/* Divider */}
        <div className="flex items-center text-center my-6 text-gray-400 text-sm font-medium">
          <div className="flex-1 border-b border-gray-200 dark:border-gray-600"></div>
          <span className="px-4">OR</span>
          <div className="flex-1 border-b border-gray-200 dark:border-gray-600"></div>
        </div>

        {/* Google Button */}
        <button
          onClick={handleGoogleSignIn}
          className="w-full py-3.5 px-4 bg-white dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-xl text-[15px] font-semibold text-gray-700 dark:text-gray-200 cursor-pointer transition-all duration-200 flex items-center justify-center gap-3 mb-4 hover:border-gray-300 dark:hover:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-600 hover:shadow-md"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Continue with Google
        </button>

        {/* Forgot Password */}
        {isLogin && (
          <p className="text-center m-0">
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                console.log("Forgot password");
              }}
              className="text-primary-purple no-underline text-sm font-medium transition-colors duration-200 hover:text-primary-purple-dark hover:underline"
            >
              Forgot your password?
            </a>
          </p>
        )}
      </div>
    </div>
  );
};

export default Login;
