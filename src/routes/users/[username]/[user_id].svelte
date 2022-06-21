<script context="module">
    export async function load({params}){
        return {props: {username: params.username, user_id: params.user_id}}
    }
</script>

<script>
    import {supabase} from "$lib/supabaseClient"
    import QRCode from "$lib/QRJS.svelte"
    import { page } from "$app/stores"

    export let user_id
    export let username

    let loading = true
    let previousAttendance = false
    const user = supabase.auth.user()

    async function getOrganizerEvents() {
        try {
            const user = supabase.auth.user()

            let { data, error, status } = await supabase
                .from('events')
                .select(`id, name`)
                .eq('organizer_id', user.id)
                .single()

            if (error && status !== 406) throw error

            if (data) {
                return data
            }
        } catch (error) {
            alert(error.message)
        }
    }

    async function getPreviousAttendance(eventId, userId) {
        console.log(eventId, userId)
        let { data: activities, error } = await supabase
            .from('activities')
            .select('id')
            .eq('user_id', userId)
            .eq('entity_id', eventId)

        if (error){
            alert(error.message)
        } else {
            console.log(activities)
            previousAttendance = activities.length > 0
            return previousAttendance
        }
    }

    async function registerAttendee(eventId, userId){
        console.log(eventId, userId)
        try {
            const updates = {
                kind: "EVENT_ATTENDANCE",
                points: 10,
                url: `/events/${eventId}`,
                user_id: userId,
                entity_id: eventId
            }

            let { error } = await supabase.from('activities').insert(updates, {
                returning: 'minimal', // Don't return the value after inserting
            })

            if (error) throw error
            previousAttendance = true
        } catch (error) {
            alert(error.message)
        } finally {
            loading = false
        }
    }
</script>

<div class="container">
    {#if user}
        <h1 class="mb-5">QR Code for {username}</h1>
        {#if user.id === user_id}
            <p>Have the event organizer scan this code to attend the event</p>
            <QRCode codeValue={$page.url} squareSize="400" />
        {:else}
            {#await getOrganizerEvents()}
                <p>Getting your events...</p>
            {:then event}
                {#await getPreviousAttendance(event.id, user_id)}
                    <p>Checking if this person has already attended...</p>
                {:then attendance}
                    {#if previousAttendance}
                        <h4>{username} is attending this event!</h4>
                    {:else}
                        <button class="btn btn-primary" on:click={() => registerAttendee(event.id, user_id)}>Click here to register this attendee</button>
                    {/if}
                {/await}
            {/await}
        {/if}
    {:else}
        Not found. <a href="/static">Return to home.</a>
    {/if}
</div>
