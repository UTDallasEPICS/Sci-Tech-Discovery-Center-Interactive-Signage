function Button({ mainText, subText, color, onClick, disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`font-title rounded-2xl relative overflow-hidden h-full w-full
                  text-white border-2 border-solid px-8
                  m-10 text-6xl transition-opacity
                  ${disabled ? "opacity-50 cursor-not-allowed" : color}`}
    >
      <div className="flex items-center justify-center">
        <h3>{mainText}</h3>
      </div>
      <span className="absolute left-2 bottom-2 text-base font-title">
        {subText}
      </span>
    </button>
  );
}

export default Button;
