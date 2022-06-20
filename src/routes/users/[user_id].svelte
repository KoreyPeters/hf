<script context="module">
    export async function load({params}){
        return {props: {user_id: params.user_id}}
    }
</script>

<script>
    import {supabase} from "$lib/supabaseClient"
    import QRCode from "$lib/QRJS.svelte"
    import { page } from "$app/stores"

    export let user_id
    const user = supabase.auth.user()
</script>

{#if user}
    {#if user.id === user_id}
        <p>Have the event organizer scan this code to attend the event</p>
        <QRCode codeValue={$page.url} squareSize="400" />
    {:else}
        This is where we would to stuff to register someone.
    {/if}
{:else}
    Not found. <a href="/">Return to home.</a>
{/if}

