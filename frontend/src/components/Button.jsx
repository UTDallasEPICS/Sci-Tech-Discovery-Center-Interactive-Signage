function Button({mainText, subText, color}){
    return(
        <button 
            className={`font-title rounded-2xl relative overflow-hidden h-full w-full
                      text-white border-2 border-solid px-8
                        m-10 text-6xl ${color}`}>
                
                <div className="flex items-center justify-center">
                    <h3 className="">
                    {mainText}
                    </h3>
                </div>

                <span className="absolute left-2 bottom-2 text-base font-title">
                    {subText}
                </span>
        </button>
    )
}
export default Button