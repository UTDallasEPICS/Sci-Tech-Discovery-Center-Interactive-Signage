import React from "react";
import SlowMotionArrow from "./UI components/SlowMotionArrow";
import kidsScanning from "../assets/kids_scanning.png";

export default function ScanPage() {
  return (
    <div className="w-full h-screen relative bg-lang-bg bg-contain">
        <div className="absolute left-20 top-72">
            <h1 className="text-center text-white text-9xl font-title">
                Scan Here
            </h1>
        </div>

        <div className="absolute left-20 bottom-52">
            <SlowMotionArrow/>
        </div>
        <div className="absolute left-72 bottom-52">
            <SlowMotionArrow/>
        </div>
        

        <div className="absolute right-0 top-0 m-5 rounded-2xl">
            <img src={kidsScanning} className="w-[600px] rounded-2xl max-h-sm object-contain"/>

        </div>
    </div>
  );
}