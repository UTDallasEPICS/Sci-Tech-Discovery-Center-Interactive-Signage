// components/WelcomeScreen.jsx
import Button from "./Button";

const LangaugeSelect = () => {
  return (
    <div className="w-full h-screen grid grid-rows-12 justify-evenly bg-lang-bg bg-contain">
      <h1 className="text-center text-white text-9xl row-start-3 row-end-5 font-title">
        Welcome
      </h1>
      <h3 className="text-center text-white text-4xl row-start-5 row-end-6 mt-5 font-subtitle">
        to the Human Machine
      </h3>
      
      <div className="flex justify-evenly h-full w-full row-start-6 row-end-8">
        <Button mainText={"English"} subText={"English"} color="bg-gradient-to-br from-rose-500 to-pink-500" />
        <Button mainText={"Español"} subText={"Spanish"} color="bg-orange" />
        <Button mainText={"తెలుగు"} subText={"Telugu"} color="bg-gradient-to-br from-purple-500 to-indigo-500" />
      </div>
      <h4 className="text-center text-white text-5xl row-start-10 row-end-11 font-subtitle">
        Choose your language to explore the amazing human body
      </h4>
    </div>
  );
};

export default LangaugeSelect;