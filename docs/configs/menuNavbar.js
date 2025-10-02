import {
    mdiMenu,
    mdiClockOutline,
    mdiCloud,
    mdiCrop,
    mdiAccount,
    mdiCogOutline,
    mdiEmail,
    mdiLogout,
    mdiThemeLightDark,
    mdiGithub,
    mdiReact
  } from '@mdi/js'
  
  export default [
    {
      // icon: mdiMenu,
      label: 'Home',
    },
    {
      // icon: mdiMenu,
      label: 'Plan Trip',
      href: '/chatbot',
    },
    {
      // icon: mdiMenu,
      label: 'Resources',
      href: '/dashboard',
    },
    {
      // icon: mdiMenu,
      label: 'Pricing',
      href: '/',
    },
    {
      // icon: mdiMenu,
      label: 'Travel Blog',
      href: '/',
    },
    {
      isCurrentUser: true,
      menu: [
        {
          icon: mdiAccount,
          label: 'My Profile',
          to: '/profile'
        },
        {
          icon: mdiCogOutline,
          label: 'Settings'
        },
        {
          icon: mdiEmail,
          label: 'Messages'
        },
        {
          isDivider: true
        },
        {
          icon: mdiLogout,
          label: 'Log Out',
          isLogout: true
        }
      ]
    },
    {
      icon: mdiThemeLightDark,
      label: 'Light/Dark',
      isDesktopNoLabel: true,
      isToggleLightDark: true
    },
  ]
  