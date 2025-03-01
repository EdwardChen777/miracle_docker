import React from 'react'
import logo from '../assets/logo.svg'

const Navbar = () => {
  return (
    <nav className='w-full flex items-center py-5 fixed top-0 z-20 bg-[#262735]' >
        <div className='w-full flex justify-between items-center mx-10'>
            <div>
                <img src={logo} className='w-12 h-12 object-contain'/>
            </div>

            <a className={`'text-white' hover:text-white transition duration-200 ease-in-out text-[18px] font-semibold font-technor cursor-pointer nav-hover-btn` } >
                Miracle
            </a>
        </div>
        
      </nav>
  )
}

export default Navbar