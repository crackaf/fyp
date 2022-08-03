import { DropdownProps } from "components/Navbar/components/Dropdown";

export const navbarDropdownButtons: DropdownProps[] = [
  {
    header: "WATERMARK",
    dropdownItems: [
      {
        name: "Image",
        link: "/watermark-image",
      },
      {
        name: "Video",
        link: "/watermark-video",
      },
    ],
  },
  {
    header: "AUTHENTICATE",
    dropdownItems: [
      {
        name: "Image",
        link: "/authenticate-image",
      },
      {
        name: "Video",
        link: "/authenticate-video",
      },
    ],
  },
  {
    header: "RECOVER",
    dropdownItems: [
      {
        name: "Image",
        link: "/recover-image",
      },
      {
        name: "Video",
        link: "/recover-video",
      },
    ],
  },
];
