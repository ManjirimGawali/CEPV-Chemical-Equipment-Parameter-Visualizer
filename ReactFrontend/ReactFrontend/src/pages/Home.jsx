import React from 'react'
import MyButton from '../components/MyButton'

const Home = () => {
  return (
    <>
        <div >

            {/* <button style={{
                color:"red",
                backgroundColor:"black",
                padding:"14px",
                borderRadius:"10px",
                margin:"29px"
            }} >
                Starting React
            </button>
            <button style={{
                color:"red",
                backgroundColor:"black",
                padding:"14px",
                borderRadius:"10px",
                margin:"29px"
            }} >
                Ending React
            </button> */}

            <MyButton buttonName={"Normal "} buttonColor={"green"} />
            <MyButton buttonName={"Original"} buttonColor={"yellow"}
             textcolor={"black"} />
            <MyButton buttonName={"Ending "} buttonColor={"red"} />
            <MyButton buttonName={"Starting "} buttonColor={"blue"} />
            <MyButton buttonName={"Paglu "} buttonColor={"pink"} 
            textcolor='black' />
            

            

        </div>
    
    
    
    </>
  )
}

export default Home
