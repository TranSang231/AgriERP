<template>
  <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
    <div v-if="!authenticated" class="lg:py-20 py-6">
      <LoginForm>
        <div class="flex text-center justify-center">
          <AmozLogo class="h-20" />
        </div>
        <div class="my-5">
          <p class="lg:text-l text-center font-bold">
            {{ $t("welcome_to_amoz") }}
          </p>
        </div>
      </LoginForm>
    </div>
    <div v-else class="w-full">
      <TopbarNav />
      <div class="pt-50">
        <slot />
      </div>
      <footer class="w-full bg-gray-100 flex justify-center">
        <FooterContent />
      </footer>
    </div>

    <div class="widget">
      <div class="chat_header">
        <!--Add the name of the bot here -->
        <span class="chat_header_title">Alpha</span>
        <span class="dropdown-trigger" href="#" data-target="dropdown1">
          <More/>
        </span>

        <!-- Dropdown menu-->
        <ul id="dropdown1" class="dropdown-content">
          <li><a href="#" id="clear">Clear</a></li>
          <li><a href="#" id="restart">Restart</a></li>
          <li><a href="#" id="close">Close</a></li>
        </ul>
      </div>

      <!--Chatbot contents goes here -->
      <div class="chats" id="chats">
        <div class="clearfix"></div>
      </div>

      <!--keypad for user to type the message -->
      <div class="keypad">
        <textarea
          id="userInput"
          placeholder="Type a message..."
          class="usrInput"
        ></textarea>
        <div id="sendButton">
          <i class="fa fa-paper-plane" aria-hidden="true"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AmozLogo from "~/assets/icons/Logo.svg";
import { More } from "@element-plus/icons-vue";
import { useOauthStore } from "@/stores/oauth";
const oauthStore = useOauthStore();
const authenticated = computed(() => {
  const { tokenInfo } = oauthStore;
  if (!tokenInfo) return false;
  const { access_token } = tokenInfo;
  if (!access_token) return false;
  return access_token.length > 0;
});
</script>
