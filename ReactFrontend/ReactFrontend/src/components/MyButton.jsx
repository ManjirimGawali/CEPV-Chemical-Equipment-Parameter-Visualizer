import React from "react";

const MyButton = ({ buttonName, buttonColor, textcolor = "white" }) => {
  return (
    <>
      <button
        style={{
          margin: "10px",
          backgroundColor: buttonColor,
          padding: "10px",
          color: textcolor,
          borderRadius: "10px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.5)",
          fontFamily: "Arial, sans-serif",
        }}
        className="hover"
      >
        I am {buttonName}
      </button>
    </>
  );
};

export default MyButton;
