import React from "react";
import styled from "styled-components";

const DropdownBtn = styled.button`
  color: #fffffff1;
  font-size: 17px;
  background-color: transparent;
  border: none;
  margin-top: 6px;
  margin-right: 8px;
`;

const DropdownMenu = styled.ul`
  background-color: #3fa1cb;
  font-size: 18px;
`;

const DropdownMenuItem = styled.a`
  color: white;
  font-size: 18px;
  :hover {
    background-color: #75b2cd;
    color: white;
  }
`;

export interface DropdownProps {
  header: string;
  dropdownItems: {
    name: string;
    link: string;
  }[];
}

function DropdownButton(dropdownContent: DropdownProps) {
  return (
    <div className="dropdown">
      <DropdownBtn
        type="button"
        className="dropdown-toggle"
        data-bs-toggle="dropdown"
      >
        {dropdownContent.header}
      </DropdownBtn>
      <DropdownMenu className="dropdown-menu">
        {dropdownContent.dropdownItems.map((item, index) => (
          <li key={index}>
            <DropdownMenuItem className="dropdown-item" href={item.link}>
              {item.name}
            </DropdownMenuItem>
          </li>
        ))}
      </DropdownMenu>
    </div>
  );
}

export default DropdownButton;
