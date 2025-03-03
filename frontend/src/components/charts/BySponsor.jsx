import React from 'react'
import { useEffect, useState } from "react";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BySponsor = () => {

    const [trialsBySponsor, setTrialsBySponsor] = useState([]);
    
    useEffect(() => {
        fetch("http://localhost:8000/api/trials-by-sponsor") // Thanks to proxy, this hits FastAPI
        .then(response => response.json())
        .then(data => {setTrialsBySponsor(data.slice(0, 10)); console.log('fetched trials by sponsor')})
        .catch(error => console.error("Error fetching data:", error));
    }, []);

  return (
    <div className='w-full h-full'>
        <ResponsiveContainer width="100%" height="100%" className="pt-10">
            <BarChart
            width={500}
            height={300}
            data={trialsBySponsor}
            margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 70,
            }}
            >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
                dataKey="sponsor" 
                angle={-20}  // Rotate the labels by 45 degrees
                textAnchor="end"  // Align the labels to the right (end)
                interval={0}  // Ensure all labels are shown (you can change this for better fit)
                tick={{ fontSize: 10 }}
            />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" activeBar={<Rectangle fill="pink" stroke="blue" />} />
            </BarChart>
        </ResponsiveContainer>
    </div>
  )
}

export default BySponsor