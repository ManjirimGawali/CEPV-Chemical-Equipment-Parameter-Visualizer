import React from "react";

const Footer = () => {
  return (
    <footer className="rounded-2xl text-slate-300 mt-16">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Top section */}
        <div className="flex flex-col md:flex-row justify-center items-center gap-6">
          {/* Brand */}
          <div className="text-center md:text-left">
            <h3 className="text-lg font-semibold text-slate-600">
              Chemical Equipment Parameter Visualizer
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Data analytics & visualization for chemical equipment
            </p>
          </div>

          {/* Links */}
        </div>

        {/* Divider */}
        <div className="border-t border-slate-300 my-2"></div>

        <div className="text-center font-semibold text-slate-700">
          Created by Manjiri Gawali (VIT Bhopal)
        </div>
      </div>
    </footer>
  );
};

export default Footer;
