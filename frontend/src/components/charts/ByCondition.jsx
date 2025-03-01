import React from 'react'
import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';

const ByCondition = () => {
    const [trialsByCondition, setTrialsByCondition] = useState([]);

    useEffect(() => {
      fetch("/api/trials-by-condition") // Thanks to proxy, this hits FastAPI
        .then(response => response.json())
        .then(data => {setTrialsByCondition(data.slice(0, 10))})
        .catch(error => console.error("Error fetching data:", error));
    }, []);

  return (
    <div className='w-full h-full'>
        <ResponsiveContainer width="90%" height="90%" >
            <PieChart width={500} height={500}>
                {/* First Pie Chart (Outer Circle) */}
                <Pie
                    dataKey="count"
                    isAnimationActive={false}
                    data={trialsByCondition}
                    cx="50%"
                    cy="50%"
                    outerRadius={140}
                    fill="#8884d8"
                    label = {({ conditions }) => conditions}
                />
            </PieChart>
        </ResponsiveContainer>
    </div>
  )
}

export default ByCondition