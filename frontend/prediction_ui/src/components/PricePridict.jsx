import axios from 'axios';
import { useState } from 'react';
const PricePredict = () => {
    const [houseData,setHouseData]=useState({
        size: '',
        bedrooms: '',
        age: ''
    });
const [price,setPrice]=useState(null);
const handleChange=(e)=>{
    const {name,value}=e.target;
    setHouseData({
        ...houseData,
        [name]:value
    });
}
const submitHandler= async(e)=>{
    e.preventDefault();
    if(!houseData.size || !houseData.bedrooms || !houseData.age){
        alert("Please fill all the fields");
        return;
    }   
    try {
        const response = await axios.post('http://localhost:8000/api/predict/', houseData);
        setPrice(response.data.predicted_price); 
    } catch (error) {
        
        console.error("There was an error predicting the price:", error);
    }
}

  return (
    <div className="min-h-screen bg-black text-slate-100 flex items-center justify-center px-4">
      <div className="w-full max-w-xl rounded-xl border border-gray-800 bg-gray-950 shadow-2xl shadow-cyan-900/30 p-2">
          <div className='bg-gray-950/70 p-4 rounded-lg mb-6'>
            <h1 className="text-3xl font-mono font-bold text-center">House Price Predictor</h1>
            <p className="text-slate-400 mt-1 text-sm text-center   ">Enter property details to estimate market value.</p>
          </div>
        <form className="space-y-4 mx-6" onSubmit={submitHandler} >
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-200">House Size (sq ft)</label>
            <input
              className="w-2/3 rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-slate-100 outline-none ring-0 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30 transition"
              type="number"
              min={0}
              name='size'
              required
              onChange={handleChange}
              value={houseData.size}
              placeholder="e.g. 1800"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-200">Number of bedrooms</label>
            <input
              className="w-2/3 rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-slate-100 outline-none ring-0 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30 transition"
              type='number'
              min={0}
              name="bedrooms"
              required
              onChange={handleChange}
              value={houseData.bedrooms}
              placeholder="e.g. 3"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-200">House Age (years)</label>
            <input
              className="w-2/3 rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-slate-100 outline-none ring-0 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30 transition"
              type='number'
              min={0}
              name="age"
              required
              onChange={handleChange}
              value={houseData.age}
              placeholder="e.g. 8"
            />
          </div>
            <div className="flex justify-end">
              <button
                className="inline-flex items-center gap-2 rounded-xl  text-gray-100 font-semibold p-3 bg-black border hover:bg-gray-800"
                type='submit'
              >
                Predict Price
              </button>
            </div>
        </form>
        {
            price !== null && (
                <div>
                <h2 className="mt-6 text-2xl font-semibold">Estimated Price: ${price.toFixed(2)}</h2>
                    </div>
            )
        }
      </div>
    </div>
    
  )
}
export default PricePredict;