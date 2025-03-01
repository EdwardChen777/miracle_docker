import React from 'react'
import ByCondition from './charts/ByCondition'
import BySponsor from './charts/BySponsor'
import { useEffect, useState } from "react";

const Dashboard = () => {
  
  const [usTrials, setUsTrials] = useState([]);
  const [euTrials, setEuTrials] = useState([]);
  // const [usRowSpan, setUsRowSpan] = useState(5);
  // const [euRowSpan, setEuRowSpan] = useState(5);
      
  useEffect(() => {
      fetch("/api/total-trials") // Thanks to proxy, this hits FastAPI
      .then(response => response.json())
      .then(data => {
        console.log(data)
        const usTrials = data[0].total;
        const euTrials = data[1].total;
        const total = usTrials + euTrials;
        

        // Calculate proportions for column span of 10
        let usSpan = Math.round((usTrials / total) * 10); 
        let euSpan = 10 - usSpan; 

        // Ensure usSpan doesn't exceed 8 and euSpan doesn't go below 2
        if (usSpan > 8) {
          usSpan = 8;
          euSpan = 2;
        } else if (euSpan < 2) {
          euSpan = 2;
          usSpan = 8;
        }
        console.log(usSpan)
        console.log(euSpan)

        setUsTrials(usTrials);
        setEuTrials(euTrials);
        setUsRowSpan(usSpan);
        setEuRowSpan(euSpan);
      })
      .catch(error => console.error("Error fetching data:", error));
  }, []);


  return (
    <div className='w-screen h-screen bg-[#262735] pt-20'>
        <div className="grid grid-rows-5 grid-cols-10 gap-4 h-full p-4">

        <div className={`bg-[#323448] text-white flex flex-col items-start justify-center col-span-5 row-span-1 rounded-md pl-10`}>
          <h1 className='text-xl font-bold'>
            {usTrials}
          </h1>
          <p className='text-sm text-gray-300'>
            ClinicalTrials.gov
          </p>
        </div>

        <div className={`bg-[#323448] text-white flex flex-col items-start justify-center col-span-5 row-span-1 rounded-md pl-10`}>
          <h1 className='text-xl font-bold'>
            {euTrials}
          </h1>
          <p className='text-sm text-gray-300'>
            EudraCT Trials
          </p>
        </div>

        <div className="bg-[#323448] text-white flex flex-col items-start justify-center col-span-5 row-span-4 rounded-md">
          <p className='text-md text-gray-300 pt-10 pl-10'>
            Clinical Trials by Conditions
          </p>
          <ByCondition />
        </div>

        <div className="bg-[#323448] text-black flex flex-col items-start justify-center col-span-5 row-span-4 rounded-md">
          <p className='text-md text-gray-300 pt-10 pl-10'>
            Clinical Trials by Sponsor
          </p>
          <BySponsor />
        </div>
      </div>


    </div>
  )
}

export default Dashboard