import * as React from "react";
import styled from "styled-components";
import { Breadcrumbs, Link } from "@mui/material";

const BCContainer = styled.div`
  height: 80px;
  width: 100%;
  display: flex;
  padding: 0;
  align-items: center;
  box-shadow: 0px 3px 2px -1px #cfcfcf;
`;

function HeaderBreadcrumb({ breadcrumbItems }: { breadcrumbItems: any }) {
  return (
    <BCContainer>
      <Breadcrumbs className="fs-5 ms-4">
        {breadcrumbItems.map((item: any) => {
          return (
            <Link key={item.name} href={item.href}>
              {item.name}
            </Link>
          );
        })}
      </Breadcrumbs>
    </BCContainer>
  );
}

export default HeaderBreadcrumb;
